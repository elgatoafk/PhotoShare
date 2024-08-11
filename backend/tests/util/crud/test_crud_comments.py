import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException
from backend.src.util.crud.comment import (create_comment, get_comments, update_comment, get_comment_by_id, delete_comment, get_user_comment)
from backend.src.util.crud.photo import get_photo
from backend.src.util.schemas.comment import CommentCreate, CommentUpdate
from backend.src.util.models.comment import Comment
from backend.src.util.models.photo import Photo
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
def mock_db ():
	return MagicMock (spec=AsyncSession)

@pytest.fixture
def mock_photo ():
	photo = MagicMock (spec=Photo)
	photo.id = 1
	return photo

@pytest.fixture
def mock_comment ():
	comment = MagicMock (spec=Comment)
	comment.id = 1
	comment.content = 'Sample comment'
	comment.photo_id = 1
	comment.user_id = 1
	return comment

@pytest.mark.asyncio
async def test_create_comment (mock_db, mock_photo, mock_comment):
	with patch ('backend.src.util.crud.comment.get_photo', AsyncMock (return_value=mock_photo)):
		mock_db.execute = AsyncMock (return_value=MagicMock (scalars=AsyncMock (return_value=[])))
		mock_db.add = AsyncMock ()
		mock_db.commit = AsyncMock ()
		mock_db.refresh = AsyncMock ()

		comment_create = CommentCreate (content='New comment')
		result = await create_comment (mock_db, comment_create, user_id=1, photo_id=1)

		assert result.content == 'New comment'

		expected_comment = Comment (content='New comment', photo_id=1, user_id=1)

		mock_db.add.assert_called_once ()
		added_comment = mock_db.add.call_args[0][0]
		assert added_comment.content == expected_comment.content
		assert added_comment.photo_id == expected_comment.photo_id
		assert added_comment.user_id == expected_comment.user_id

		mock_db.commit.assert_called_once ()
		mock_db.refresh.assert_called_once ()

@pytest.mark.asyncio
async def test_get_comments (mock_db, mock_photo, mock_comment):
	with patch ('backend.src.util.crud.comment.get_photo', AsyncMock (return_value=mock_photo)):
		mock_db.execute = AsyncMock (return_value=MagicMock (scalars=AsyncMock (return_value=[mock_comment])))

		result = await get_comments (mock_db, photo_id=1)

		assert len (result) == 1
		assert result[0].content == 'Sample comment'
		get_photo.assert_called_once_with (mock_db, photo_id=1)
		mock_db.execute.assert_called_once ()

@pytest.mark.asyncio
async def test_update_comment (mock_db, mock_comment):
	mock_db.execute = AsyncMock (return_value=MagicMock (scalars=AsyncMock (return_value=[mock_comment])))
	mock_db.commit = AsyncMock ()
	mock_db.refresh = AsyncMock ()

	updated_comment = CommentUpdate (content='Updated comment content')
	result = await update_comment (mock_db, comment_id=1, comment=updated_comment)

	assert result.content == 'Updated comment content'
	assert mock_comment.content == 'Updated comment content'
	assert mock_comment.updated_at is not None
	mock_db.commit.assert_called_once ()
	mock_db.refresh.assert_called_once ()

@pytest.mark.asyncio
async def test_get_comment_by_id (mock_db, mock_comment):
	mock_db.execute = AsyncMock (return_value=MagicMock (scalars=AsyncMock (return_value=[mock_comment])))
	result = await get_comment_by_id (mock_db, comment_id=1)

	assert result.content == 'Sample comment'
	mock_db.execute.assert_called_once ()

@pytest.mark.asyncio
async def test_get_comment_by_id_not_found (mock_db):
	mock_db.execute = AsyncMock (return_value=MagicMock (scalars=AsyncMock (return_value=[])))

	with pytest.raises (HTTPException) as excinfo:
		await get_comment_by_id (mock_db, comment_id=1)

	assert excinfo.value.status_code == 404
	assert excinfo.value.detail == "Comment not found"

@pytest.mark.asyncio
async def test_delete_comment (mock_db, mock_comment):
	with patch ('backend.src.util.crud.comment.get_comment_by_id', AsyncMock (return_value=mock_comment)):
		mock_db.delete = AsyncMock ()
		mock_db.commit = AsyncMock ()

		result = await delete_comment (mock_db, comment_id=1)

		assert result.content == 'Sample comment'
		get_comment_by_id.assert_called_once_with (mock_db, comment_id=1)
		mock_db.delete.assert_called_once_with (mock_comment)
		mock_db.commit.assert_called_once ()

@pytest.mark.asyncio
async def test_get_user_comment (mock_db, mock_comment):
	mock_db.execute = AsyncMock (return_value=MagicMock (scalars=AsyncMock (return_value=[mock_comment])))
	result = await get_user_comment (mock_db, user_id=1, comment_id=1)

	assert result.content == 'Sample comment'
	mock_db.execute.assert_called_once ()

@pytest.mark.asyncio
async def test_get_user_comment_not_found (mock_db):
	mock_db.execute = AsyncMock (return_value=MagicMock (scalars=AsyncMock (return_value=[])))

	with pytest.raises (HTTPException) as excinfo:
		await get_user_comment (mock_db, user_id=1, comment_id=1)

	assert excinfo.value.status_code == 404
	assert excinfo.value.detail == "Comment not found"