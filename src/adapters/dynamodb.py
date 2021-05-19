import boto3
import json

class DDB:
    def __init__(self, table):
        self.client = boto3.client("dynamodb")
        self.table = table

    def get(self, k, v):
        response = self.client.get_item(
            TableName=self.table,
            Key={
                k: { "S": v }
            }
        )["Item"]
        return response

    def scan(self, k):
        response = self.client.scan(
            TableName=self.table
        )["Items"]
        return response
    
    def put(self, item):
        response = self.client.put_item(
            TableName=self.table,
            Item = item
        )
        return response
