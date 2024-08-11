import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from backend.src.config.security import get_current_user, get_current_active_user
from backend.src.util.models.user import User

@pytest.mark.asyncio
async def test_get_current_user_success ():
	mock_user = User (email="test@example.com", hashed_password="hashedpassword", is_active=True)
	db = AsyncMock ()

	with patch ("backend.src.config.security.get_user_by_email", return_value=mock_user), patch ("backend.src.config.jwt.jwt.decode",
	                                                                                             return_value={"sub": "test@example.com"}):
		result = await get_current_user (token="fake_token", db=db)

	assert result.email == mock_user.email

@pytest.mark.asyncio
async def test_get_current_user_user_not_found ():
	db = AsyncMock ()

	with patch ("backend.src.config.security.get_user_by_email", return_value=None), patch ("backend.src.config.jwt.jwt.decode",
	                                                                                        return_value={"sub": "test@example.com"}):
		with pytest.raises (HTTPException) as exc_info:
			await get_current_user (token="fake_token", db=db)

	assert exc_info.value.status_code == 401

@pytest.mark.asyncio
async def test_get_current_active_user_inactive ():
	mock_user = User (email="test@example.com", hashed_password="hashedpassword", is_active=False)

	with patch ("backend.src.config.security.get_current_user", return_value=mock_user):
		with pytest.raises (HTTPException) as exc_info:
			await get_current_active_user (current_user=mock_user)

	assert exc_info.value.status_code == 400
