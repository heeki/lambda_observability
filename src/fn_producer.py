import boto3
import json
import os
import redis
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
from datetime import datetime

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

# function: external calls
def send_message(payload):
    response = client.send_message(
        QueueUrl=queue_url,
        MessageBody=payload
    )
    return response

def rset(k, v):
    return redis_connection.set(k, json.dumps(v))

def rget(k):
    output = redis_connection.get(k)
    output = json.loads(output.decode("utf-8")) if output is not None else None
    return output

def rdelete(k):
    return redis_connection.delete(k)

# function: lambda invoker handler
def handler(event, context):
    print(json.dumps(event))

    body = json.loads(event["body"])
    event_id = body["id"]
    print(json.dumps(body))
    response = send_message(json.dumps(body))
    print(json.dumps(response))
    status = response["ResponseMetadata"]["HTTPStatusCode"]
    message_id = response["MessageId"]

    now = datetime.today().isoformat()
    subsegment = xray_recorder.begin_subsegment("Redis")
    subsegment.put_annotation("EventId", event_id)
    previous = rget(event_id)
    rset(event_id, now) if redis_enabled else None
    xray_recorder.end_subsegment()

    subsegment = xray_recorder.begin_subsegment("GenerateResponse")
    subsegment.put_annotation("MessageId", message_id)
    payload = {
        "event_id": event_id,
        "event_body": body["message"],
        "sqs_message_id": message_id,
        "ts_previous": previous,
        "ts_current": now
    }
    response = build_response(status, json.dumps(payload))
    print(json.dumps(response))
    xray_recorder.end_subsegment()
    return response

# initialization, mapping
patch_all()
client = boto3.client("sqs")
queue_url = os.environ["QUEUE_URL"]
redis_enabled = os.environ["REDIS_ENABLED"] == "true"
redis_endpoint = os.environ["REDIS_ENDPOINT"]
try:
    if redis_enabled:
        redis_connection = redis.Redis(
            host=redis_endpoint,
            port=6379,
            db=0,
            socket_timeout=5
        )
except redis.ConnectionError as e:
    print(e)