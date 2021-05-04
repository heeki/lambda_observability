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

# function: lambda invoker handler
def handler(event, context):
    print(json.dumps(event))

    subsegment = xray_recorder.begin_subsegment("CustomSubsegment")
    subsegment.put_annotation("tbd", "tbd")
    response = json.dumps(event)
    xray_recorder.end_subsegment()
    return response

# initialization, mapping
initialization()
