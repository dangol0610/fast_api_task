from unittest.mock import AsyncMock
import pytest


@pytest.mark.api
async def test_get_posts(client, mocker):
    expected_response = [{"id": 1, "title": "Test Post"}]
    mock_service = mocker.patch(
        "task.apps.api_integration.service.APIService.get_posts",
        AsyncMock(return_value=expected_response),
    )
    response = client.get("/api/other/posts")
    assert response.status_code == 200
    assert response.json() == expected_response
    mock_service.assert_awaited_once()
