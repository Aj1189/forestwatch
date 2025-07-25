import json
import boto3
import os
import re
import requests

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
sns = boto3.client('sns')
sqs = boto3.client('sqs')

MODERATION_THRESHOLD = 80.0
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']
SQS_QUEUE_URL = os.environ['SQS_QUEUE_URL']
REJECTION_API_URL = os.environ['REJECTION_API_URL']

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Get image bytes from S3
    image_bytes = s3.get_object(Bucket=bucket, Key=key)['Body'].read()

    # Detect moderation labels
    response = rekognition.detect_moderation_labels(
        Image={'Bytes': image_bytes}
    )
    labels = response.get('ModerationLabels', [])
    print("Detected Labels:", labels)

    flagged = [label for label in labels if label['Confidence'] > MODERATION_THRESHOLD]

    if flagged:
        print("Flagged Content Detected:", flagged)

        # 1. Delete from S3
        s3.delete_object(Bucket=bucket, Key=key)

        # 2. Push JSON to SQS
        sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps({
                "action": "ImageDeletedDueToModeration",
                "key": key,
                "bucket": bucket,
                "labels": flagged
            })
        )

        # 3. Send SNS alert
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="ForestWatch - Image Moderation Alert",
            Message=f"Image '{key}' uploaded to bucket '{bucket}' was deleted due to content violation. Labels: {json.dumps(flagged)}"
        )

        complaint_id = key
        if complaint_id:
            try:
                reason_labels = [
                    f"{label['Name']} (Confidence: {round(label['Confidence'], 2)}%)"
                    for label in flagged
                ]
                reason = "Image rejected due to policy violation: " + ", ".join(reason_labels)

                callback_data = {
                    "complaint_id": complaint_id,
                    "reason": reason
                }
                headers = { "Content-Type": "application/json" }
                response = requests.post(REJECTION_API_URL, data=json.dumps(callback_data), headers=headers)
                print("Callback API response:", response.status_code, response.text)
            except Exception as e:
                print("Callback API call failed:", str(e))
        else:
            print("Complaint ID could not be extracted from key:", key)

    return {
        'statusCode': 200,
        'body': json.dumps('Moderation check completed.')
    }
