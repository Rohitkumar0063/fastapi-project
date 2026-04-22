import pytest
from httpx import AsyncClient, ASGITransport
from mongomock_motor import AsyncMongoMockClient
from main import app
import routes
import auth

@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    mock_client = AsyncMongoMockClient()
    mock_db = mock_client["myapp"]
    monkeypatch.setattr(routes, "user_collection", mock_db["users"])
    monkeypatch.setattr(routes, "order_collection", mock_db["orders"])
    monkeypatch.setattr(auth, "user_collection", mock_db["users"]) 
@pytest.fixture
async def client(mock_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c