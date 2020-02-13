from pg_client.pg_client import PGClient
from pg_client.credentials import DB_CREDENTIALS

query = "SELECT 1"
client = PGClient(credentials=DB_CREDENTIALS)
con = client.create_connection()
print(client.execute_query(con,query))