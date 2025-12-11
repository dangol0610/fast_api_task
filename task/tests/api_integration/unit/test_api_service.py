from unittest.mock import AsyncMock, Mock
import pytest

from task.apps.api_integration.service import APIService


@pytest.mark.service
async def test_get_posts(mocker):
    fake_json = [{"id": 1, "titel": "test"}]

    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json = Mock(return_value=fake_json)

    fake_client = AsyncMock()
    fake_client.get = AsyncMock(return_value=fake_response)

    fake_redis = AsyncMock()
    fake_redis.get = AsyncMock(return_value=None)
    fake_redis.set = AsyncMock()

    result = await APIService.get_posts(client=fake_client, redis=fake_redis)
    assert result == fake_json
    fake_client.get.assert_awaited_once_with(
        "https://jsonplaceholder.typicode.com/posts"
    )
