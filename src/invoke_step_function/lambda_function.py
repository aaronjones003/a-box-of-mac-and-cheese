import boto3
import json
import os

def lambda_handler(event, context):
    """
    Initiate a Step Functions execution for book cover generation
    """
    try:
        state_machine_arn = os.environ.get('STATE_MACHINE_ARN')
        
        if not state_machine_arn:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'STATE_MACHINE_ARN not configured'})
            }
        
        client = boto3.client('stepfunctions')
        response = client.start_execution(
            stateMachineArn=state_machine_arn
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'executionArn': response.get('executionArn')
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }