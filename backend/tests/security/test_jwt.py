from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.config.jwt import create_access_token, verify_token
from backend.src.util.schemas.user import TokenData

@pytest.mark.asyncio
async def test_create_access_token():
    db = AsyncMock(spec=AsyncSession)
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    data = {"sub": "test@example.com"}
    token = await create_access_token(data, user_id=1, db=db)
    assert isinstance(token, str)

@pytest.mark.asyncio
async def test_verify_token ():
    db = AsyncMock ()

    with patch ("backend.src.config.jwt.jwt.decode", return_value={"sub": "test@example.com"}):
        token = "fake_token"
        result = verify_token (token, db=db)

        assert isinstance (result, TokenData)
        assert result.email == "test@example.com"