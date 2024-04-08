import boto3
import json

def lambda_handler(event, context):
    client = boto3.client('stepfunctions')
    response = client.start_execution(
        stateMachineArn='arn:aws:states:us-east-1:214054894798:stateMachine:MyStateMachine-s4gn5s12v',
    )

    return response.get('executionArn')