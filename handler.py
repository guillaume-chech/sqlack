
import os
import json
from pg_client.pg_client import PGClient
from utils.lambda_logger import LambdaLogger
from urllib.parse import parse_qs
# from tabulate import tabulate


def endpoint(event, context):
    """[summary]

    Arguments:
        event {[type]} -- [description]
        context {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    # LambdaLogger().setup(os.environ['LOG_LEVEL'], context)
    logger = LambdaLogger()
    logger.info({
        'message': 'Received Sqlack command',
        'event': event
    })
    creds = {'host': os.environ['DB_HOST'], 'db_name': os.environ['DB_NAME'], 'port': os.environ['DB_PORT'],
             'username': os.environ['DB_USERNAME'], 'password': os.environ['DB_PASSWORD']}
    print(creds)
    try:
        print(event)
        params = parse_qs(event['body'])
        query = params.get('text', [None])[0]
        print(query)
        client = PGClient(creds)
        result = client.execute_query(query)
        response = {
            'statusCode': 200,
            'body': json.dumps(result),
            'headers': {
                'Content-Type': 'application/json',
            },
            # "result": tabulate(tabular_data=result["data"], headers=result["headers"], tablefmt="psql")
        }
        return response

    except Exception as e:
        response = {
            'statusCode': 400,
            'body': 'Invalid query :  {}'.format(e),
            'headers': {
                'Content-Type': 'application/json'},
        }
        return response
