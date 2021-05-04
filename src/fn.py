import boto3
import json
import os
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

# function: initialization
def initialization():
    patch_all()

# function: heloer
def build_response(code, body):
    # headers for cors
    headers = {
        "Access-Control-Allow-Origin": "amazonaws.com",
        "Access-Control-Allow-Credentials": True
    }
    # lambda proxy integration
    response = {
        'isBase64Encoded': False,
        'statusCode': code,
        'headers': headers,
        'body': body
    }
    return response

# function: custom logic
def send_message(payload):
    response = client.send_message(
        QueueUrl=queue_url,
        MessageBody=payload
    )
    return response

# function: lambda invoker handler
def handler(event, context):
    print(json.dumps(event))

    response = send_message(json.dumps(event["body"]))
    print(json.dumps(response))

    status = response["ResponseMetadata"]["HTTPStatusCode"]
    message = "hello"
    response = build_response(status, "success")
    print(json.dumps(response))

    return response

# initialization, mapping
client = boto3.client('sqs')
queue_url = os.environ['QUEUE_URL']
initialization()
