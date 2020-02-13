from pg_client.pg_client import PGClient
from pg_client.credentials import DB_CREDENTIALS
from tabulate import tabulate

query = "SELECT id,created_at from backend.users limit 10"
client = PGClient(credentials=DB_CREDENTIALS)
result = client.execute_query(query)
print(tabulate(tabular_data=result["data"],headers=result["headers"],tablefmt="psql"))