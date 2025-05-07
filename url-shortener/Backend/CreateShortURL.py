import json
import boto3
import random
import string
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'URLTable')
table = dynamodb.Table(table_name)

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def lambda_handler(event, context):
    body = json.loads(event['body'])
    long_url = body.get('longURL')

    if not long_url:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "longURL is required"})
        }

    short_code = generate_short_code()

    table.put_item(
        Item={
            'shortCode': short_code,
            'longURL': long_url
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
           "shortURL": f"https://4z20f7m73b.execute-api.us-east-1.amazonaws.com/{short_code}"
        })
    }
