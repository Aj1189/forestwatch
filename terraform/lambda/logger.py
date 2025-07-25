import os
import json
import boto3
import uuid
from datetime import datetime

AUDIT_TABLE = os.environ['AUDIT_TABLE']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(AUDIT_TABLE)

def lambda_handler(event, context):
    for record in event['Records']:
        message_body = json.loads(record['body'])

        item = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow().isoformat(),
            'action': message_body.get('action'),
            'bucket': message_body.get('bucket'),
            'key': message_body.get('key'),
            'labels': json.dumps(message_body.get('labels', [])),
        }

        table.put_item(Item=item)
        print("Logged to DynamoDB:", item)

    return {
        'statusCode': 200,
        'body': json.dumps('SQS message logged to DynamoDB')
    }
