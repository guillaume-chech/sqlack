
import os
import json
import boto3
import requests
from botocore.exceptions import ClientError
from pg_client.pg_client import PGClient
from utils.lambda_logger import LambdaLogger
from urllib.parse import parse_qs
from tabulate import tabulate


def gateway(event, context):
    """[summary]

    Arguments:
        event {[type]} -- [description]
        context {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    LambdaLogger().setup(os.environ['LOG_LEVEL'], context)
    logger = LambdaLogger()
    logger.info({
        'message': 'Received Sqlack command from Slack',
        'event': event
    })

    cmd_params = parse_qs(event['body'])
    query = cmd_params.get('text', [None])[0].replace('`', '')

    logger.info({
        'message': 'Query to be forwarded to runner',
        'query': query
    })

    try:
        client = boto3.client('lambda')

        client.invoke(
            FunctionName='sqlack-dev-sqlackRunner',
            InvocationType='Event',
            LogType='None',
            ClientContext='None',
            Payload=json.dumps({'cmd_params': cmd_params,
                                'query': query})
        )
        logger.info({
            'message': 'Invoked runner, waiting exiting'
        })
        response = {
            'statusCode': 200,
            'body': json.dumps("Executing query : /n ```{}```".format(query)),
            'headers': {
                'Content-Type': 'application/json',
            }
        }
        return response
    except ClientError as e:
        logger.exception({
            'message': 'raised exception invoking Runner function',
            'response_error': e.response['Error'],
            'operation_name': e.operation_name,
            'response_metadata': e.response['ResponseMetadata']
        })
        response = {
            'statusCode': 400,
            'body': 'Something went wrong, that is all I can say :  {}'.format(e),
            'headers': {
                'Content-Type': 'application/json'},
        }
        return response


def query_runner(event, context):
    """[summary]

    Arguments:
        event {[type]} -- [description]
        context {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    LambdaLogger().setup(os.environ['LOG_LEVEL'], context)
    logger = LambdaLogger()
    logger.info({
        'message': 'Received Sqlack command from gateway',
        'event': event
    })
    creds = {'host': os.environ['DB_HOST'], 'db_name': os.environ['DB_NAME'], 'port': os.environ['DB_PORT'],
             'username': os.environ['DB_USERNAME'], 'password': os.environ['DB_PASSWORD']}
    cmd_params = event['cmd_params']
    response_url = cmd_params['response_url'][0]

    try:
        query = event['query']
        client = PGClient(creds)
        logger.info({
            'message': 'Executing query',
            'query': query
        })

        result = client.execute_query(query)
        response_body = {
            'response_type': 'in_channel',
            'text': "```" + tabulate(tabular_data=result["data"], headers=result["headers"], tablefmt="psql") + "```"
        }

        requests.post(response_url, json=response_body)

        return response_body

    except Exception as e:
        response_url = cmd_params['response_url'][0]
        response_body = {
            'response_type': 'in_channel',
            'text': 'Invalid query :  {}'.format(e)
        }
        requests.post(response_url, json=response_body)
        return response_body
