import pytest
from fastapi_admin.file_upload import FileUpload
from fastapi_admin.exceptions import FileExtNotAllowed, FileMaxSizeLimit
from starlette.datastructures import UploadFile
import aiofiles
import os
from unittest.mock import AsyncMock, Mock


@pytest.fixture
async def file_upload():
    os.makedirs('/tmp/uploads', exist_ok=True)
    return FileUpload(uploads_dir='/tmp/uploads')


@pytest.mark.asyncio
async def test_init(file_upload):
    file_upload = await file_upload
    assert file_upload.uploads_dir == '/tmp/uploads'
    assert file_upload.allow_extensions == None
    assert file_upload.max_size == 1024**3
    assert file_upload.filename_generator == None
    assert file_upload.prefix == '/static/uploads'


@pytest.mark.asyncio
async def test_save_file(file_upload, tmp_path):
    file_upload = await file_upload
    filename = 'test.txt'
    content = b'hello world'
    expected_path = os.path.join('/static/uploads', filename)
    result_path = await file_upload.save_file(filename, content)
    assert result_path == expected_path
    async with aiofiles.open(os.path.join('/tmp/uploads', filename), 'rb') as f:
        read_content = await f.read()
    assert read_content == content


@pytest.mark.asyncio
async def test_upload_within_size_limit(file_upload, tmp_path):
    file_upload = await file_upload
    file = Mock(UploadFile)
    file.filename = 'test.txt'
    file.read = AsyncMock(return_value=b'hello world')
    result_path = await file_upload.upload(file)
    expected_path = os.path.join('/static/uploads', 'test.txt')
    assert result_path == expected_path


@pytest.mark.asyncio
async def test_upload_exceeding_size_limit(file_upload, tmp_path):
    file_upload = await file_upload
    file_upload.max_size = 5
    file = Mock(UploadFile)
    file.filename = 'test.txt'
    file.read = AsyncMock(return_value=b'hello world')
    with pytest.raises(FileMaxSizeLimit):
        await file_upload.upload(file)


@pytest.mark.asyncio
async def test_upload_disallowed_extension(file_upload, tmp_path):
    file_upload = await file_upload
    file_upload.allow_extensions = ['.exe']
    file = Mock(UploadFile)
    file.filename = 'test.txt'
    file.read = AsyncMock(return_value=b'hello world')
    with pytest.raises(FileExtNotAllowed):
        await file_upload.upload(file)
