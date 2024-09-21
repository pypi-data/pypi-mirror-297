import json
from unittest.mock import patch
from python_asana.api import AsanaAPI
from python_asana import config


class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        pass


def mock_requests_get(sample_data_page1, sample_data_page2=None):
    def mocked_requests_get(url, headers):
        if sample_data_page2 and "offset=token_for_page_2" in url:
            return MockResponse(sample_data_page2)
        else:
            return MockResponse(sample_data_page1)

    return mocked_requests_get


def test_query_asana_single_page():
    config.base_url = "https://app.asana.com/api/1.0"

    # Sample data for a single page with no pagination
    sample_data = {
        "data": [
            {"gid": "1", "name": "Task 1", "assignee": "User A"},
            {"gid": "2", "name": "Task 2", "assignee": "User B"},
        ],
        "next_page": None,  # No next page
    }

    with patch("requests.get", side_effect=mock_requests_get(sample_data)):
        query = "/projects/1234567890/tasks?opt_fields=gid,name,assignee"
        asana_bearer_token = "test_token"

        asana_api = AsanaAPI(api_key=asana_bearer_token)
        result = asana_api.query_asana(query)

        expected_data = sample_data["data"]
        expected_result = json.dumps(expected_data)

        assert result == expected_result


def test_query_asana_empty_data():
    config.base_url = "https://app.asana.com/api/1.0"

    sample_data = {"data": [], "next_page": None}

    with patch("requests.get", side_effect=mock_requests_get(sample_data)):
        query = "/projects/1234567890/tasks?opt_fields=gid,name,assignee"
        asana_bearer_token = "test_token"

        asana_api = AsanaAPI(api_key=asana_bearer_token)
        result = asana_api.query_asana(query)

        expected_data = sample_data["data"]
        expected_result = json.dumps(expected_data)
        assert result == expected_result
