from psycopg2.pool import ThreadedConnectionPool
import logging

class Database():
    def __init__(self, config):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

        self._pool = ThreadedConnectionPool(1, 10, 
                database=config['DB_DATABASE'],
                user=config['DB_USER'],
                password=config['DB_PASSWORD'],
                host=config['DB_HOST'],
                async=False)

    def get_connection(self):
        return self._pool.getconn()

    def put_away_connection(self, con):
        self._pool.putconn(con)
