import boto3
import json
import os
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

# function: initialization
def initialization():
    patch_all()

# function: helper
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

    body = json.loads(event["body"])
    print(json.dumps(body))
    response = send_message(json.dumps(body))
    print(json.dumps(response))
    status = response["ResponseMetadata"]["HTTPStatusCode"]
    message_id = response["MessageId"]

    subsegment = xray_recorder.begin_subsegment("CustomSubsegment")
    subsegment.put_annotation("MessageId", message_id)
    payload = {
        "event_id": body["id"],
        "event_body": body["message"],
        "sqs_message_id": message_id,
    }
    response = build_response(status, json.dumps(payload))
    print(json.dumps(response))
    xray_recorder.end_subsegment()
    return response

# initialization, mapping
client = boto3.client("sqs")
queue_url = os.environ["QUEUE_URL"]
initialization()
