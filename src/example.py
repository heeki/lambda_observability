import boto3
import json
import os
from lib.response import success, failure
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all


# function: custom logic
def send_message(payload):
    response = client.send_message(
        QueueUrl=queue_url,
        MessageBody=payload
    )
    return response


# function: initialization
def initialization():
    patch_all()


# function: lambda invoker handler
def handler(event, context):
    print(json.dumps(event))

    response = send_message(json.dumps(event["body"]))
    print(json.dumps(response))

    status = response["ResponseMetadata"]["HTTPStatusCode"]
    if status == 200:
        response = success("success")
    else:
        response = failure("failure")
    print(json.dumps(response))

    return response


# initialization, mapping
client = boto3.client('sqs')
queue_url = os.environ['QUEUE_URL']
initialization()

