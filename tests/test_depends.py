import pytest
from fastapi import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from tortoise import Tortoise
from unittest.mock import AsyncMock, MagicMock

from fastapi_admin.depends import get_model, get_model_resource, get_resources, get_redis, get_current_admin, _get_resources
from fastapi_admin.exceptions import InvalidResource
from fastapi_admin.resources import Dropdown, Link, Model, Resource


@pytest.fixture
def mock_request():
    request = MagicMock(spec=Request)
    request.app = MagicMock()
    request.state.admin = None
    return request


def test_get_model_valid_resource():
    Tortoise.apps = {'models': {'valid_resource': 'model'}}
    model = get_model('valid_resource')
    assert model == 'model'


def test_get_model_invalid_resource():
    Tortoise.apps = {'models': {'valid_resource': 'model'}}
    model = get_model('invalid_resource')
    assert model is None


@pytest.mark.asyncio
async def test_get_model_resource_valid(mock_request):
    mock_request.app.get_model_resource.return_value = MagicMock(spec=Model)
    mock_request.app.get_model_resource.return_value.get_actions = AsyncMock(return_value=[])
    mock_request.app.get_model_resource.return_value.get_bulk_actions = AsyncMock(return_value=[])
    mock_request.app.get_model_resource.return_value.get_toolbar_actions = AsyncMock(return_value=[])
    model_resource = await get_model_resource(mock_request)
    assert model_resource.toolbar_actions == []
    assert model_resource.actions == []
    assert model_resource.bulk_actions == []


@pytest.mark.asyncio
async def test_get_model_resource_invalid(mock_request):
    mock_request.app.get_model_resource.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        await get_model_resource(mock_request)
    assert excinfo.value.status_code == HTTP_404_NOT_FOUND


def test_get_resources(mock_request):
    class MockLink(Link):
        icon = 'icon'
        label = 'label'
        url = 'url'
        target = '_blank'
    class MockModel(Model):
        icon = 'icon'
        label = 'label'
        model = MagicMock(__name__='model')
    class MockDropdown(Dropdown):
        icon = 'icon'
        label = 'label'
        resources = []
    mock_request.app.resources = [MockLink, MockModel, MockDropdown]
    resources = get_resources(mock_request)
    assert len(resources) == 3


def test_get_redis(mock_request):
    mock_request.app.redis = 'redis_instance'
    redis = get_redis(mock_request)
    assert redis == 'redis_instance'


def test_get_current_admin(mock_request):
    mock_request.state.admin = 'admin'
    admin = get_current_admin(mock_request)
    assert admin == 'admin'


def test_get_current_admin_unauthenticated(mock_request):
    with pytest.raises(HTTPException) as excinfo:
        get_current_admin(mock_request)
    assert excinfo.value.status_code == HTTP_401_UNAUTHORIZED


def test_get_resources_with_invalid_resource():
    class InvalidResourceMock(Resource):
        icon = 'icon'
        label = 'label'
    with pytest.raises(InvalidResource):
        _get_resources([InvalidResourceMock])


@pytest.mark.parametrize('resource_class, expected_type', [
    (Link, 'link'),
    (Model, 'model'),
    (Dropdown, 'dropdown')
])
def test_get_resources_with_valid_resources(resource_class, expected_type):
    class TestResource(resource_class):
        icon = 'test_icon'
        label = 'test_label'
        if resource_class == Link:
            url = 'test_url'
            target = '_blank'
        elif resource_class == Model:
            model = MagicMock(__name__='test_model')
        elif resource_class == Dropdown:
            resources = []

    resources = _get_resources([TestResource])
    assert len(resources) == 1
    assert resources[0]['type'] == expected_type