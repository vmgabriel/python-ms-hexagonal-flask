# Develop: vmgabriel

# Libraries
import psycopg2

# Absracts
from domain.models.db_connection import Db_Connection
from config.server import configuration as conf

class Postgres_Connection(Db_Connection):
    def __init__(self):
        self.conn = None
        self.cursor = None

        try:
            if not self.conn:
                self.conn = psycopg2.connect(self.connector())
            print('[DATABASE] - Database Connected')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('[DATABASE - ERROR] - ', error)


    def get_connection(self):
        return self.conn


    def get_cursor(self):
        return self.conn.cursor()


    def disconnect(self):
        try:
            self.cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
            print('DATABASE: Connection closed.')


    def connector(self, is_inicialized: bool = True)  -> str:
        db_name_database = ''
        if is_inicialized:
            db_name_database = conf['db_name_database']
        else:
            db_name_database = 'postgres'
        return 'dbname={} user={} password={} host={} port={}'.format(
            db_name_database,
            conf['user_database'],
            conf['password_database'],
            conf['host_database'],
            conf['port_database']
        )


