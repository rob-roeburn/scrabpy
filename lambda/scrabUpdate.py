import boto3, json
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    dynamoresource = boto3.resource('dynamodb')
    table = dynamoresource.Table('scrab')
    record = table.query(
        IndexName='gameId-playerId-index', 
        KeyConditionExpression=Key('gameId').eq(str(event['gameId'])) & Key('playerId').eq(str(event['playerId']))
    )
    dynamoclient = boto3.client('dynamodb')
    updatedRack = dynamoclient.update_item(
        TableName='scrab',
        Key={'id':{'S': record['Items'][0]['id']}},
        UpdateExpression='set tileRack = :tr',
        ExpressionAttributeValues={
            ':tr': {'S':str(event['tileRack'])}
        },
        ReturnValues='UPDATED_NEW'
    )

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*' },    
        'body': updatedRack

    }
