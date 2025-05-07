import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'URLTable')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    short_code = event['pathParameters']['shortCode']

    response = table.get_item(Key={'shortCode': short_code})

    if 'Item' not in response:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Short URL not found"})
        }

    long_url = response['Item']['longURL']

    return {
        "statusCode": 301,
        "headers": {
            "Location": long_url
        }
    }
