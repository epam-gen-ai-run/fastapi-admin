import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_303_SEE_OTHER
from fastapi_admin.app import app


@pytest.mark.asyncio
async def test_list_view(async_client: AsyncClient):
    response = await async_client.get('/resource/list')
    assert response.status_code == HTTP_200_OK
    # Add further assertions to validate the response content


@pytest.mark.asyncio
async def test_create_view(async_client: AsyncClient):
    response = await async_client.get('/resource/create')
    assert response.status_code == HTTP_200_OK
    # Add further assertions to validate the response content

