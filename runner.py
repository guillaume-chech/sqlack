
import os
import json
import boto3
import requests
from pg_client.pg_client import PGClient
from utils.lambda_logger import LambdaLogger
from tabulate import tabulate


def respond(response_url, data_body, err_body=None):
    """Prepare HTTP response depending on response type.
    Hit the given endpoint aftr the response is ready

    Arguments:
        response_url -- The endpoint to hit with the response
        data_body  -- The data to be sent with the response

    Keyword Arguments:
        err_body -- If an error occur , will replace the data body (default: {None})

    Returns:
        -- The result of the post request
    """
    response_body = {
        'response_type': 'in_channel',
        'text': 'Invalid query :  {}'.format(err_body) if err_body
        else "```" + tabulate(tabular_data=data_body["data"], headers=data_body["headers"], tablefmt="psql") + "```"
    }
    return requests.post(response_url, json=response_body)


def handler(event, context):
    """Handles event coming from the gateway, parses the event,  set up a PGclient, execute the query
    and then respond to Slack

    Arguments:
        event  -- The event received through SNS and sent by the gateway lambda
        context -- Always empty

    Returns:
         -- A dummy log response
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
        return respond(response_url=response_url, data_body=result, err_body=None)

    except Exception as e:
        logger.exception({
            'message': 'Encountered an error when querying DB:',
            'error': e
        })
        return respond(response_url=response_url, data_body=None, err_body=e)
