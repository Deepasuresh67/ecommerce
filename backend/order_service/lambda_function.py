import json
import boto3
import uuid
from decimal import Decimal
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('dee-orders')

def convert_decimal(obj):
    if isinstance(obj, Decimal):
        return int(obj)

def lambda_handler(event, context):

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "GET,POST,DELETE,OPTIONS"
    }

    # ✅ CORS preflight
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": ""
        }

    try:
        method = event.get("httpMethod")

        # ───────── GET ORDERS ─────────
        if method == "GET":
            params = event.get("queryStringParameters") or {}
            user_id = params.get("user_id")

            if not user_id:
                return {
                    "statusCode": 200,
                    "headers": headers,
                    "body": json.dumps([])
                }

            # 🔥 FIX: Proper filtering
            response = table.scan(
                FilterExpression=Attr("user_id").eq(user_id)
            )

            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps(response.get("Items", []), default=convert_decimal)
            }

        # ───────── CREATE ORDER ─────────
        elif method == "POST":
            body = json.loads(event.get("body", "{}"))

            order = {
                "order_id": str(uuid.uuid4()),
                "user_id": body.get("user_id"),
                "items": body.get("items", []),
                "total": body.get("total", 0)
            }

            table.put_item(Item=order)

            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({
                    "message": "Order placed",
                    "order": order
                })
            }

        # ───────── DELETE ORDER ─────────
        elif method == "DELETE":
            body = json.loads(event.get("body", "{}"))
            order_id = body.get("order_id")

            table.delete_item(Key={"order_id": order_id})

            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({"message": "Order deleted"})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }