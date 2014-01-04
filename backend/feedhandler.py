import feedparser
import configparser
import logging
import time
from backend.common import Database, get_config

class FeedHandler():
    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
        config   = get_config()
        self._DB  = Database(config)
        self._con = self._DB.get_connection()

    def update_feed(self, feed_id, feed_url=None):
        if feed_url == None:
            cur = self._con.cursor()
            cur.execute('SELECT url FROM lysr_feed WHERE id=%s', (feed_id,))
            self._con.commit()
            feed_url = cur.fetchone()[0]

        logging.info('Updating feed {}: {}'.format(feed_id, feed_url))

        feed = feedparser.parse(feed_url)
    
        new_entries = 0
        if feed.status is 200:
            try:
                cur = self._con.cursor()
    
                for entry in feed.entries:
                    # Bad HTML is removed by default
                    cur.execute('SELECT id FROM lysr_feed_entry WHERE feed = %s AND guid = %s', (feed_id, entry.link))
                    self._con.commit()
               
                    if cur.rowcount is 0:
                        new_entries += 1
                        cur.execute('INSERT INTO lysr_feed_entry (feed, guid, content, title) VALUES (%s, %s, %s, %s)',
                                (feed_id, entry.link, entry.description, entry.title))
                        self._con.commit()

                
                logging.info('Fetched feed {}, {} new entries found'.format(feed_id, new_entries))
    
            except Exception as e:
                logging.error('Database: {}'.format(str(e).split('\n')[0]))
        else:
            logging.info('Failed to fetch feed {}, status {}'.format(feed_id, feed.status))

        cur = self._con.cursor()

        cur.execute('UPDATE lysr_feed SET last_check=NOW() WHERE id=%s', (feed_id,))
        self._con.commit()

        if new_entries:
            cur.execute('UPDATE lysr_feed SET last_update=NOW() WHERE id=%s', (feed_id,))
        else:
            cur.execute('''UPDATE lysr_feed SET update_interval=LEAST(1.5*update_interval, '7d'::interval) WHERE id=%s''', (feed_id,))
        self._con.commit()


    def update_feeds(self):
        cur = self._con.cursor()
        cur.execute('SELECT id, url FROM lysr_feed WHERE NOW() > last_check + update_interval')
        self._con.commit()

        for feed in cur:
            self.update_feed(*feed)

    def handle_forever(self):
        logging.info('Starting feed handler')
        while True:
            self.update_feeds()
            time.sleep(15)
