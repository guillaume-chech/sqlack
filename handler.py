
import os
from pg_client.pg_client import PGClient
from utils.lambda_logger import LambdaLogger
from tabulate import tabulate


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
    creds = {'host':os.environ['DB_HOST'],'db_name':os.environ['DB_NAME'],'port':os.environ['DB_PORT'],'username':os.environ['DB_USERNAME'],'password':os.environ['DB_PASSWORD']}
    print(creds)
    try:
        query = event
        print(query)
        client = PGClient(creds)
        result = client.execute_query(query)
        response = {
            "statusCode": 200,
            "result": tabulate(tabular_data=result["data"], headers=result["headers"], tablefmt="psql")
        }
        return response

    except Exception as e:
        response = {
            "statusCode": 200,
            "error": "Invalid query :  {}".format(e)}
        return response
