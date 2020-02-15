
import os
import json
import boto3
from botocore.exceptions import ClientError
from utils.lambda_logger import LambdaLogger
from urllib.parse import parse_qs


def is_request_valid(cmd_params):
    is_token_valid = cmd_params['token'][0] == os.environ['SLACK_VERIFICATION_TOKEN']
    return is_token_valid


def parse_cmd_txt(cmd_txt):
    if cmd_txt is None:
        return False, "Query is empty"
    # Slack does not forward single quote as single quote unless encapsulated in code snippet
    # so we must force the user to encapsulate the query in a snippet
    if cmd_txt[0]!='`'or cmd_txt[0]!='`':
        return False, "Don't forget to pass your query with tild around it, like this `my_query`"
    return True, cmd_txt


def respond(res, err=None):
    """Prepare HTTP response depending if an error occured or not.
    Arguments:
        res -- The response body to be sent

    Keyword Arguments:
        err_body -- If an error occur , will replace the response body (default: {None})

    Returns:
        -- An http response
    """
    return {
        'statusCode': '400' if err else '200',
        'body': str(err) if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        }
    }


def handler(event, context):
    """Handles reception of slack command, parsing the content
    and sending an event to be consumed by the runner

    Arguments:
        event -- The event received on the lambda endpoint
        context {[type]} -- The context of the event received on the lambda endpoint

    Returns:
        -- An http response
    """
    LambdaLogger().setup(os.environ['LOG_LEVEL'], context)
    logger = LambdaLogger()
    logger.info({
        'message': 'Received Sqlack command from Slack',
        'event': event
    })

    cmd_params = parse_qs(event['body'])
    query_txt = cmd_params.get('text', [None])[0]

    if not is_request_valid(cmd_params):
        return respond(res=None, err="Invalid Authentication Token")
    parsed_query = parse_cmd_txt(query_txt)
    if not parsed_query[0]:
        logger.info({
            'message': 'Could not parse the query',
            'Reason': parsed_query[1]
        })
        return respond(res=parsed_query[1], err=None)
    else:
        query = parsed_query[1]
        logger.info({
            'message': 'Query to be forwarded to runner',
            'query': query[1]
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
            res = "Executing query : ```{}```".format(query)
            return respond(res)

        except ClientError as e:
            logger.exception({
                'message': 'raised exception invoking Runner function',
                'response_error': e.response['Error'],
                'operation_name': e.operation_name,
                'response_metadata': e.response['ResponseMetadata']
            })
            return respond(res=None, err=e)
