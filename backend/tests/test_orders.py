from unittest.mock import patch, MagicMock

with patch("boto3.resource") as mock_dynamo:
    mock_table = MagicMock()
    mock_dynamo.return_value.Table.return_value = mock_table

    from product_service.lambda_function import lambda_handler
import os
os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-1"
import json
from unittest.mock import patch
from order_service.lambda_function import lambda_handler

@patch("order_service.lambda_function.table")
def test_get_orders(mock_table):
    mock_table.scan.return_value = {
        "Items": [{"order_id": "1", "user_id": "u1"}]
    }

    event = {
        "httpMethod": "GET",
        "queryStringParameters": {"user_id": "u1"}
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200

@patch("order_service.lambda_function.table")
def test_create_order(mock_table):
    event = {
        "httpMethod": "POST",
        "body": json.dumps({
            "user_id": "u1",
            "items": [],
            "total": 100
        })
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200


@patch("order_service.lambda_function.table")
def test_delete_order(mock_table):
    event = {
        "httpMethod": "DELETE",
        "body": json.dumps({"order_id": "1"})
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200