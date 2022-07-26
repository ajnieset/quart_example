from typing import AsyncGenerator

import pytest
from quart import Quart

from quart_example.app import create_app


@pytest.fixture(name="app", scope="function")
async def _app() -> AsyncGenerator[Quart, None]:
    app = create_app()
    async with app.test_app():
        yield app
