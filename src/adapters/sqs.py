import boto3
import json

class SQS:
    def __init__(self, queue_url):
        self.client = boto3.client("sqs")
        self.queue_url = queue_url

    def send(self, payload):
        response = self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=payload
        )
        return response
