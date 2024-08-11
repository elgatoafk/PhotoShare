import sys

from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import pytest
import asyncio

from httpx import AsyncClient

from backend.main import app

client = TestClient (app)

@pytest.mark.asyncio
async def test_signup ():
	user_data = {"email": "test@example.com", "password": "testpassword"}
	with patch ("backend.src.util.crud.user.create_user", new_callable=AsyncMock) as mock_create_user:
		mock_create_user.return_value = None
		response = client.post ("/signup", json=user_data)
		assert response.status_code == 201



@pytest.mark.asyncio
async def test_login():
    unique_email = "test@example.com"
    user_data = {"username": unique_email, "password": "testpassword"}

    # Patch the dependencies
    with patch("backend.src.util.crud.user.get_user_by_email", return_value=AsyncMock(is_active=True)), \
         patch("backend.src.config.hash.hash_handler.verify_password", return_value=True), \
         patch("backend.src.config.jwt.create_access_token", return_value="fake_token"):

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/login", data=user_data)

            # Check the response
            assert response.status_code == 200
            assert response.json() == {"access_token": "fake_token", "token_type": "bearer"}