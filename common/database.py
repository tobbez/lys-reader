import psycopg2
import configparser
import logging

__all__ = ['DB']

class Database():
    def __init__(self):
        config = configparser.ConfigParser(interpolation=None)
        config.read(('config.ini',))

        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

        try:
            self.connection = psycopg2.connect(
                    database=config.get('database', 'database'), 
                    user=config.get('database', 'user'),
                    password=config.get('database', 'password'),
                    host=config.get('database', 'host'), 
                    async=False)
        except psycopg2.OperationalError as e:
            logging.error('Database: {}'.format(str(e).split('\n')[0]))
            raise Exception("Unable to connect to database")

DB = Database()
