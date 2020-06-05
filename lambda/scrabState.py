import boto3, json
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('scrab')
    response = table.query(
        IndexName='gameId-playerId-index', 
        KeyConditionExpression=Key('gameId').eq(str(event['pathParameters']['gameId'])) & Key('playerId').eq(str(event['pathParameters']['playerId']))
    )
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*' },    
        'body': json.dumps(response)
    }
