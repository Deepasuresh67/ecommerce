import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('dee-cart')

# Convert Decimal to int/float
def convert_decimal(obj):
    if isinstance(obj, Decimal):
        return int(obj)

def lambda_handler(event, context):

    try:
        method = event.get("httpMethod")

        # GET CART ITEMS
        if method == "GET":
            response = table.scan()

            return {
                "statusCode": 200,
                "body": json.dumps(response.get("Items", []), default=convert_decimal)
            }

        # ADD ITEM TO CART
        elif method == "POST":
            body = json.loads(event.get("body", "{}"))

            item = {
                "user_id": body.get("user_id"),
                "product_id": body.get("product_id"),
                "quantity": body.get("quantity")
            }

            table.put_item(Item=item)

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Item added to cart",
                    "item": item
                })
            }

        # DELETE ITEM
        elif method == "DELETE":
            body = json.loads(event.get("body", "{}"))

            user_id = body.get("user_id")

            table.delete_item(
                Key={
                    "user_id": user_id
                }
            )

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Item removed from cart"
                })
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }