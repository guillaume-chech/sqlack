# from pg_client.pg_client import PGClient
# from pg_client.credentials import DB_CREDENTIALS
# from tabulate import tabulate

# query = "SELECT id,created_at from backend.users limit 10"
# client = PGClient(credentials=DB_CREDENTIALS)
# result = client.execute_query(query)
# print(tabulate(tabular_data=result["data"],headers=result["headers"],tablefmt="psql"))

import requests
import json

result = {'text':"1"}
response_body = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': json.dumps(result)
            # "result": tabulate(tabular_data=result["data"], headers=result["headers"], tablefmt="psql")
        }
response_url = "https://hooks.slack.com/commands/T3BBXAR7F/954499312070/EvqAWTN1LEFqWOfFF8keJcaX"


rq = requests.post(response_url, json=response_body)
print(rq)
