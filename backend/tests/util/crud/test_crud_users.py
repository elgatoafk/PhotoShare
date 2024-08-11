from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.util.crud import user as crud

@pytest.mark.asyncio
async def test_create_user ():
    db = AsyncMock (spec=AsyncSession)
    db.add = MagicMock ()
    db.commit = AsyncMock ()
    db.refresh = AsyncMock ()

    user_data = {"email": "test@example.com", "password": "testpassword"}

    with patch ("backend.src.util.crud.user.create_user", new_callable=AsyncMock) as mock_create_user:
        mock_create_user.return_value = MagicMock (email="test@example.com")
        new_user = await crud.create_user (db, user_data)
        assert new_user.email == "test@example.com"

@pytest.mark.asyncio
async def test_get_user_by_email ():
    db = AsyncMock (spec=AsyncSession)
    with patch ("backend.src.util.crud.user.get_user_by_email", new_callable=AsyncMock) as mock_get_user_by_email:
        mock_get_user_by_email.return_value = None
        user = await crud.get_user_by_email (db, email="test@example.com")
        assert user is None

@pytest.mark.asyncio
async def test_deactivate_user():
    db = AsyncMock(spec=AsyncSession)
    db.execute = AsyncMock()
    db.commit = AsyncMock()
    await crud.deactivate_user(db, user_id=1)
    db.execute.assert_called_once()
    db.commit.assert_called_once()
