import psycopg2
from psycopg2 import extras
from utils.lambda_logger import LambdaLogger

class PGClient(object):
    def __init__(self,credentials):
        self.credentials={'host':credentials['host'],
        'db_name': credentials['db_name'],
        'port':credentials['port'],
        'user_name':credentials['user_name'],
        'password':credentials['password']
         }
        self.logger = LambdaLogger()

    def create_connection(self):
        creds = self.credentials
        try:
            con=psycopg2.connect(dbname=creds['db_name'], host=creds['host'], 
                                port=creds['port'], user=creds['user_name'], 
                                password=creds['password'])
            return con
        except Exception as e:
            print(e)
            raise
    
    def execute_query(self, con, query):
        try:
            cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(query)
            con.commit()
            result = cur.fetchall()
        except Exception as e:
            print(e)
            result = []
        finally:
            con.close()
        return result