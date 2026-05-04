import json
import boto3
import os
from decimal import Decimal
from boto3.dynamodb.conditions import Key

# DynamoDB setup
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])   # ✅ Use TABLE_NAME env var

# Convert Decimal → int (handles nested structures too)
def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(i) for i in obj]
    if isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return int(obj)
    return obj

def lambda_handler(event, context):

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
    }

    # ✅ Handle CORS preflight
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": ""
        }

    try:
        method = event.get("httpMethod")

        # ───────── GET REVIEWS ─────────
        if method == "GET":
            params = event.get("queryStringParameters") or {}
            product_id = params.get("product_id")

            if not product_id:
                return {
                    "statusCode": 400,
                    "headers": headers,
                    "body": json.dumps({"error": "product_id is required"})
                }

            response = table.query(
                KeyConditionExpression=Key("product_id").eq(int(product_id))
            )

            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps(convert_decimal(response.get("Items", [])))
            }

        # ───────── ADD REVIEW ─────────
        elif method == "POST":
            body = json.loads(event.get("body", "{}"))

            product_id = body.get("product_id")
            user_id    = body.get("user_id")
            rating     = body.get("rating")
            review     = body.get("review")

            # 🔥 VALIDATION
            if not all([product_id, user_id, rating, review]):
                return {
                    "statusCode": 400,
                    "headers": headers,
                    "body": json.dumps({"error": "All fields are required"})
                }

            if not (1 <= int(rating) <= 5):
                return {
                    "statusCode": 400,
                    "headers": headers,
                    "body": json.dumps({"error": "Rating must be between 1 and 5"})
                }

            # 🔥 Check duplicate review
            existing = table.get_item(
                Key={
                    "product_id": int(product_id),
                    "user_id": user_id
                }
            )

            if "Item" in existing:
                return {
                    "statusCode": 400,
                    "headers": headers,
                    "body": json.dumps({"error": "User already reviewed this product"})
                }

            # ✅ Save review
            item = {
                "product_id": int(product_id),
                "user_id": user_id,
                "rating": int(rating),
                "review": review
            }

            table.put_item(Item=item)

            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({"message": "Review added successfully"})
            }

        else:
            return {
                "statusCode": 405,
                "headers": headers,
                "body": json.dumps({"error": "Method not allowed"})
            }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }
