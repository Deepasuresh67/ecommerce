from unittest.mock import patch, MagicMock

with patch("boto3.resource") as mock_dynamo:
    mock_table = MagicMock()
    mock_dynamo.return_value.Table.return_value = mock_table

    from product_service.lambda_function import lambda_handler
import os
os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-1"
import json
from unittest.mock import patch, MagicMock
from product_service.lambda_function import lambda_handler

# ───── TEST GET PRODUCTS ─────
@patch("product_service.lambda_function.table")
def test_get_products(mock_table):
    mock_table.scan.return_value = {
        "Items": [{"product_id": 1, "name": "Shirt", "price": 100}]
    }

    event = {"httpMethod": "GET"}

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body[0]["name"] == "Shirt"


# ───── TEST ADD PRODUCT ─────
@patch("product_service.lambda_function.table")
def test_add_product(mock_table):
    event = {
        "httpMethod": "POST",
        "body": json.dumps({
            "product_id": 1,
            "name": "Shoes",
            "price": 500
        })
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Product added"


# ───── TEST MISSING PRODUCT ID ─────
def test_missing_product_id():
    event = {
        "httpMethod": "POST",
        "body": json.dumps({"name": "Item"})
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 400