import os
import pytest
from unittest.mock import patch, MagicMock

os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-1"

@pytest.fixture(autouse=True)
def mock_dynamodb():
    with patch("boto3.resource") as mock_resource:
        mock_table = MagicMock()
        mock_resource.return_value.Table.return_value = mock_table
        yield mock_table