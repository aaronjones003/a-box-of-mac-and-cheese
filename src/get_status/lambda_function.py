import boto3
import json

def lambda_handler(event, context):
    """
    Get the status of a Step Functions execution
    """
    try:
        body = json.loads(event.get('body', '{}'))
        execution_arn = body.get('arn')
        
        if not execution_arn:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Missing execution ARN'})
            }
        
        client = boto3.client('stepfunctions')
        response = client.describe_execution(executionArn=execution_arn)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'status': response['status'],
                'output': response.get('output', '{}')
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
