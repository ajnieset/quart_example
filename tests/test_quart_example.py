from quart_example import UserIn, app


async def test_health() -> None:
    test_client = app.test_client()
    response = await test_client.get("/health")
    data = await response.get_json()
    assert data == {"status": "healthy"}


async def test_create_user() -> None:
    test_client = app.test_client()
    response = await test_client.post(
        "/users/",
        json=UserIn(username="test_user", email="user@test.io", password="test"),
    )
    data = await response.get_json()
    assert data == {
        "id": data["id"],
        "username": "test_user",
        "email": "user@test.io",
        "password": "test",
    }
