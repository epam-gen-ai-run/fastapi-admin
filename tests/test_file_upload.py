import pytest
from fastapi_admin.file_upload import FileUpload
from fastapi_admin.exceptions import FileExtNotAllowed, FileMaxSizeLimit
from starlette.datastructures import UploadFile
import aiofiles
import os
from unittest.mock import AsyncMock, Mock


@pytest.fixture
async def file_upload():
    return FileUpload(uploads_dir='/tmp/uploads')


@pytest.mark.asyncio
async def test_init(file_upload):
    file_upload = await file_upload
    assert file_upload.uploads_dir == '/tmp/uploads'
    assert file_upload.allow_extensions == None
    assert file_upload.max_size == 1024**3
    assert file_upload.filename_generator == None
    assert file_upload.prefix == '/static/uploads'


