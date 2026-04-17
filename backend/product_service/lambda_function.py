import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('dee-products')

def convert_decimal(obj):
    if isinstance(obj, Decimal):
        return int(obj)

def lambda_handler(event, context):
    print("EVENT:", json.dumps(event))           # ✅ VERY IMPORTANT
    print("HTTP METHOD:", event.get("httpMethod"))

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "GET,POST,DELETE,OPTIONS"
    }

    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": ""
        }

    method = event.get("httpMethod")

    if method == "GET":
        response = table.scan()
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(response.get("Items", []), default=convert_decimal)
        }

    elif method == "POST":
        body = json.loads(event.get("body", "{}"))
        product_id = body.get("product_id") or body.get("id")

        if not product_id:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"error": "product_id required"})
            }

        item = {
            "product_id": int(product_id),
            "name": body.get("name"),
            "price": body.get("price")
        }

        table.put_item(Item=item)
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "added", "product": item})
        }

    elif method == "DELETE":
        print("✅ DELETE BLOCK HIT")

        body = json.loads(event.get("body", "{}"))
        product_id = body.get("product_id") or body.get("id")

        if not product_id:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"error": "product_id required"})
            }

        table.delete_item(Key={"product_id": int(product_id)})

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "message": "deleted",
                "product_id": product_id
            })
        }

    else:
        print("❌ METHOD NOT MATCHED:", method)
        return {
            "statusCode": 405,
            "headers": headers,
            "body": json.dumps({"error": "Method not allowed"})
        }