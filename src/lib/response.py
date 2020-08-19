import json


def success(body):
    return build_response(200, body)


def failure(body):
    return build_response(500, body)


def build_response(code, body):
    # headers for cors
    headers = {
        "Access-Control-Allow-Origin": "*",
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
