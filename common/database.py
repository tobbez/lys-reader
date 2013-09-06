import psycopg2
import logging
from common import config

class Database():
    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

        try:
            self.connection = psycopg2.connect(
                    database=config['DB_DATABASE'],
                    user=config['DB_USER'],
                    password=config['DB_PASSWORD'],
                    host=config['DB_HOST'],
                    async=False)
        except psycopg2.OperationalError as e:
            logging.error('Database: {}'.format(str(e).split('\n')[0]))
            raise Exception("Unable to connect to database")

