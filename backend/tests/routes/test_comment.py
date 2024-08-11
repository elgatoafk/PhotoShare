import pytest
from httpx import AsyncClient
from fastapi import FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, patch

from backend.src.routes.comment import router as comment_router
from backend.src.util.models.comment import Comment
from backend.src.util.models.photo import Photo
from backend.src.util.models.user import User, UserRole
from backend.src.util.crud.comment import create_comment, update_comment, delete_comment, get_comments, get_user_comment, get_comment_by_id
from backend.src.util.crud.photo import get_photo
from backend.src.config.security import get_current_user

@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(comment_router)
    return app

@pytest.fixture
async def mock_get_db():
    async def mock_get_db_session():
        mock_db = AsyncMock(AsyncSession)
        return mock_db
    return mock_get_db_session

@pytest.fixture
async def mock_get_current_user():
    async def mock_get_current_user_func():
        return User(id=1, email="user@example.com", role=UserRole.USER, hashed_password="hashed_password")
    return mock_get_current_user_func

@pytest.mark.asyncio
@patch('backend.src.routes.comment.get_photo', new_callable=AsyncMock)
@patch('backend.src.routes.comment.create_comment', new_callable=AsyncMock)
async def test_create_photo_comment(mock_create_comment: AsyncMock, mock_get_photo: AsyncMock, app: FastAPI, mock_get_db: AsyncMock, mock_get_current_user: AsyncMock):
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Prepare mock data
        mock_get_photo.return_value = Photo(id=1, content="Sample photo")
        mock_create_comment.return_value = Comment(id=1, content="New comment", photo_id=1, user_id=1)

        # Mock database session methods
        mock_db_session = mock_get_db()
        mock_db_session.return_value.execute = AsyncMock()
        mock_db_session.return_value.commit = AsyncMock()
        mock_db_session.return_value.refresh = AsyncMock()
        mock_db_session.return_value.add = AsyncMock()

        # Successful creation
        response = await client.post(
            "/photos/1/comments/",
            json={"content": "New comment"},
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json() == {"id": 1, "content": "New comment", "photo_id": 1, "user_id": 1}

@pytest.mark.asyncio
@patch('backend.src.routes.comment.get_comments', new_callable=AsyncMock)
async def test_read_photo_comments(mock_get_comments: AsyncMock, app: FastAPI, mock_get_db: AsyncMock):
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Prepare mock data
        mock_get_comments.return_value = [
            Comment(id=1, content="First comment", photo_id=1, user_id=1),
            Comment(id=2, content="Second comment", photo_id=1, user_id=2)
        ]

        # Mock database session methods
        mock_db_session = mock_get_db()
        mock_db_session.return_value.execute = AsyncMock()

        # Successful retrieval
        response = await client.get("/photos/1/comments/")
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["content"] == "First comment"

@pytest.mark.asyncio
@patch('backend.src.routes.comment.get_user_comment', new_callable=AsyncMock)
@patch('backend.src.routes.comment.update_comment', new_callable=AsyncMock)
async def test_update_photo_comment(mock_update_comment: AsyncMock, mock_get_user_comment: AsyncMock, app: FastAPI, mock_get_db: AsyncMock, mock_get_current_user: AsyncMock):
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Prepare mock data
        mock_get_user_comment.return_value = Comment(id=1, content="Old comment", photo_id=1, user_id=1)
        mock_update_comment.return_value = Comment(id=1, content="Updated comment", photo_id=1, user_id=1)

        # Mock database session methods
        mock_db_session = mock_get_db()
        mock_db_session.return_value.execute = AsyncMock()
        mock_db_session.return_value.commit = AsyncMock()
        mock_db_session.return_value.refresh = AsyncMock()

        # Successful update
        response = await client.put(
            "/comments/1/",
            json={"content": "Updated comment"},
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json()["content"] == "Updated comment"

@pytest.mark.asyncio
@patch('backend.src.routes.comment.get_comment_by_id', new_callable=AsyncMock)
@patch('backend.src.routes.comment.delete_comment', new_callable=AsyncMock)
async def test_delete_photo_comment(mock_delete_comment: AsyncMock, mock_get_comment_by_id: AsyncMock, app: FastAPI, mock_get_db: AsyncMock, mock_get_current_user: AsyncMock):
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Prepare mock data
        mock_get_comment_by_id.return_value = Comment(id=1, content="Comment to delete", photo_id=1, user_id=1)
        mock_delete_comment.return_value = Comment(id=1, content="Comment to delete", photo_id=1, user_id=1)

        # Mock database session methods
        mock_db_session = mock_get_db()
        mock_db_session.return_value.execute = AsyncMock()
        mock_db_session.return_value.commit = AsyncMock()
        mock_db_session.return_value.delete = AsyncMock()

        # Successful deletion
        response = await client.delete(
            "/comments/1/",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200
        assert response.json()["content"] == "Comment to delete"
