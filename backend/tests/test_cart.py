from unittest.mock import patch, MagicMock

with patch("boto3.resource") as mock_dynamo:
    mock_table = MagicMock()
    mock_dynamo.return_value.Table.return_value = mock_table

    from product_service.lambda_function import lambda_handler

import os
os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-1"
import json
from unittest.mock import patch
from cart_service.lambda_function import lambda_handler

@patch("cart_service.lambda_function.table")

def test_get_cart(mock_table):
    mock_table.scan.return_value = {
        "Items": [{"user_id": "u1", "product_id": 1}]
    }

    event = {"httpMethod": "GET"}
    response = lambda_handler(event, None)

    assert response["statusCode"] == 200


@patch("cart_service.lambda_function.table")
def test_add_to_cart(mock_table):
    event = {
        "httpMethod": "POST",
        "body": json.dumps({
            "user_id": "u1",
            "product_id": 1,
            "quantity": 2
        })
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200

@patch("cart_service.lambda_function.table")
def test_delete_cart(mock_table):
    event = {
        "httpMethod": "DELETE",
        "body": json.dumps({"user_id": "u1"})
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200