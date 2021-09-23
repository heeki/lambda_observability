import json
import os
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
from datetime import datetime
from adapters.dynamodb import DDB
from adapters.redis import Redis
from adapters.sqs import SQS

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

# function: lambda invoker handler
def handler(event, context):
    print(json.dumps(event))

    body = json.loads(event["body"])
    event_id = body["id"]
    event_body = body["message"]
    print(json.dumps(body))
    response = o_sqs.send(json.dumps(body))
    print(json.dumps(response))
    status = response["ResponseMetadata"]["HTTPStatusCode"]
    message_id = response["MessageId"]

    # cache aside
    if redis_enabled:
        now = datetime.today().isoformat()
        subsegment = xray_recorder.begin_subsegment("Redis")
        subsegment.put_annotation("EventId", event_id)
        previous = o_redis.get(event_id)
        o_redis.set(event_id, now) if redis_enabled else None
        xray_recorder.end_subsegment()
    else:
        previous = datetime.today().isoformat()
        now = datetime.today().isoformat()

    # dynamodb
    item = {
        "event_id": { "S": event_id },
        "event_body": { "S": event_body }
    }
    o_ddb.put(item)

    # response
    subsegment = xray_recorder.begin_subsegment("GenerateResponse")
    subsegment.put_annotation("MessageId", message_id)
    payload = {
        "event_id": event_id,
        "event_body": event_body,
        "sqs_message_id": message_id,
        "ts_previous": previous,
        "ts_current": now
    }
    response = build_response(status, json.dumps(payload))
    print(json.dumps(response))
    xray_recorder.end_subsegment()
    return response

# initialization: xray
patch_all()
xray_daemon_address = os.environ["AWS_XRAY_DAEMON_ADDRESS"]
print("AWS_XRAY_DAEMON_ADDRESS={}".format(xray_daemon_address))

# initialization: redis
redis_enabled = os.environ["REDIS_ENABLED"] == "true"
redis_endpoint = os.environ["REDIS_ENDPOINT"]
o_redis = Redis(redis_endpoint, 5)

# initialization: dynamodb
ddb_table = os.environ["TABLE"]
o_ddb = DDB(ddb_table)

# initialization: sqs
sqs_queue_url = os.environ["QUEUE_URL"]
o_sqs = SQS(sqs_queue_url)
