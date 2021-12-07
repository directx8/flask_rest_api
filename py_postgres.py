import psycopg2
from psycopg2 import Error

class PostgresFetcher():
    def __init__(self):
        self.USER = 'postgres'
        self.PASSWORD = 'amazonlover355'
        self.HOST = '127.0.0.1'
        self.PORT = '5432'
        self.DATABASE = 'TestDB'
    
    def connect_to_db(self):
        # Connect to an existing database
        connection = psycopg2.connect(user=self.USER,
                                    password=self.PASSWORD,
                                    host=self.HOST,
                                    port=self.PORT,
                                    database=self.DATABASE)
        return connection
    def get_rows_from_db(self, rows):
        try:
            connection = self.connect_to_db()
            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Executing a SQL query
            cursor.execute('SELECT * FROM test;')
            # Fetch result
            records = cursor.fetchmany(size=rows)
            return records

        except (Exception, Error) as error:
            print('Error while connecting to PostgreSQL', error)
            
        finally:
            if (connection):
                cursor.close()
                connection.close()
                print('PostgreSQL connection is closed')
    def get_all_rows(self):
        try:
            connection = self.connect_to_db()
            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Executing a SQL query
            cursor.execute('SELECT * FROM test;')
            # Fetch result
            records = cursor.fetchall()
            return records

        except (Exception, Error) as error:
            print('Error while connecting to PostgreSQL', error)
            
        finally:
            if (connection):
                cursor.close()
                connection.close()
                print('PostgreSQL connection is closed')
    