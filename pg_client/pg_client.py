import psycopg2
from psycopg2 import extras
from utils.lambda_logger import LambdaLogger


class PGClient(object):
    """Class responsible to handle communciation with PostgreSQL databases.
    Handles establishing connection and executing query passed to the execute_query method.
    
    Arguments:
        object {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    def __init__(self, credentials):
        self.credentials = {'host': credentials['host'],
                            'db_name': credentials['db_name'],
                            'port': credentials['port'],
                            'username': credentials['username'],
                            'password': credentials['password']
                            }
        self.logger = LambdaLogger()

    def create_connection(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """
        creds = self.credentials
        try:
            con = psycopg2.connect(dbname=creds['db_name'], host=creds['host'],
                                   port=creds['port'], user=creds['username'],
                                   password=creds['password'])
            return con
        except Exception as e:
            print(e)
            raise

    def execute_query(self, query):
        """[summary]
        
        Arguments:
            query {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        try:
            con = self.create_connection()
            cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(query)
            con.commit()
            headers = [desc[0] for desc in cur.description]
            data = cur.fetchall()
            result = {"headers": headers,
                      "data": data}
            print(data)
            return result
        except Exception as e:
            print("Invalid query :  {}".format(e))
            raise
        finally:
            con.close()
