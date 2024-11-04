import pytest
from unittest.mock import Mock, AsyncMock
from fastapi import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from tortoise import Tortoise

from fastapi_admin.depends import get_model, get_model_resource, _get_resources, get_resources, get_redis, get_current_admin
from fastapi_admin.exceptions import InvalidResource
from fastapi_admin.resources import Dropdown, Link, Model, Resource


def test_get_model():
    Tortoise.apps = {'models': {'testmodel': Mock()}}
    assert get_model('testmodel') is not None
    assert get_model('invalidmodel') is None
    Tortoise.apps = {}


@pytest.mark.asyncio
async def test_get_model_resource():
    request = Mock(spec=Request)
    request.app.get_model_resource = Mock(return_value=Mock(spec=Model))
    request.app.get_model_resource().get_actions = AsyncMock(return_value=[])
    request.app.get_model_resource().get_bulk_actions = AsyncMock(return_value=[])
    request.app.get_model_resource().get_toolbar_actions = AsyncMock(return_value=[])
    model_resource = await get_model_resource(request)
    assert hasattr(model_resource, 'toolbar_actions')
    assert hasattr(model_resource, 'actions')
    assert hasattr(model_resource, 'bulk_actions')

    request.app.get_model_resource = Mock(return_value=None)
    with pytest.raises(HTTPException) as exc_info:
        await get_model_resource(request)
    assert exc_info.value.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_redis():
    request = Mock(spec=Request)
    request.app.redis = Mock()
    assert get_redis(request) is not None


@pytest.mark.asyncio
async def test_get_current_admin():
    request = Mock(spec=Request)
    request.state.admin = Mock()
    assert get_current_admin(request) is not None
    request.state.admin = None
    with pytest.raises(HTTPException) as exc_info:
        get_current_admin(request)
    assert exc_info.value.status_code == HTTP_401_UNAUTHORIZED
