import pytest
from quart import Quart


@pytest.mark.asyncio
async def test_get_user(app: Quart) -> None:
    test_client = app.test_client()
    response = await test_client.get("/users/1")
    user = await response.get_json()
    assert user["username"] == "ajnieset"
