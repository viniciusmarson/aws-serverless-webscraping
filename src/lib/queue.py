"""Module responsible for send payloads to QUEUE"""
import os
import json
import boto3

AWS_REGION = os.getenv('AWS_REGION', 'us-west-1')
AWS_ACCOUNT_ID = os.getenv('AWS_ACCOUNT_ID', '546106101945')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')


def create_sqs_queue_url(name):
    """Create a sqs queue url based on environment variables"""
    return f"https://{AWS_REGION}.queue.amazonaws.com/{AWS_ACCOUNT_ID}/{name}-{ENVIRONMENT}"


def send_payloads_to_queue(name, payloads):
    """Send data to queue"""
    sqs_client = boto3.client('sqs')

    for index, payload in enumerate(payloads):
        sqs_client.send_message(
            QueueUrl=create_sqs_queue_url(name),
            MessageBody=json.dumps({"id": str(payload)}),
            DelaySeconds=index
        )
