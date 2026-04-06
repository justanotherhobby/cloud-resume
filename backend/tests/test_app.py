import json
import unittest
from unittest.mock import MagicMock, patch


class TestLambdaHandler(unittest.TestCase):

    def _make_mock_table(self, count_value):
        mock_table = MagicMock()
        mock_table.update_item.return_value = {
            "Attributes": {"count": count_value}
        }
        return mock_table

    @patch("app.dynamodb")
    def test_returns_incremented_count(self, mock_dynamo):
        mock_dynamo.Table.return_value = self._make_mock_table(42)

        from app import lambda_handler
        result = lambda_handler({}, {})

        self.assertEqual(result["statusCode"], 200)
        body = json.loads(result["body"])
        self.assertEqual(body["count"], 42)

    @patch("app.dynamodb")
    def test_cors_header_present(self, mock_dynamo):
        mock_dynamo.Table.return_value = self._make_mock_table(1)

        from app import lambda_handler
        result = lambda_handler({}, {})

        self.assertIn("Access-Control-Allow-Origin", result["headers"])

    @patch("app.dynamodb")
    def test_dynamodb_error_returns_500(self, mock_dynamo):
        from botocore.exceptions import ClientError
        mock_table = MagicMock()
        mock_table.update_item.side_effect = ClientError(
            {"Error": {"Code": "500", "Message": "Internal error"}}, "UpdateItem"
        )
        mock_dynamo.Table.return_value = mock_table

        from app import lambda_handler
        result = lambda_handler({}, {})

        self.assertEqual(result["statusCode"], 500)


if __name__ == "__main__":
    unittest.main()