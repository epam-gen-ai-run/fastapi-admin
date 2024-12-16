import pytest
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from tortoise import Model
import redis.asyncio as redis

from fastapi_admin.app import FastAPIAdmin, app as fastapi_app
from fastapi_admin.providers import Provider
from fastapi_admin.resources import Dropdown, Model as ModelResource, Resource
from fastapi_admin.routes import router
from fastapi_admin import middlewares

@pytest.fixture
def mock_redis():
    return redis.from_url('redis://localhost:6379/0')

@pytest.fixture
def fastapi_admin_app(mock_redis):
    app = FastAPIAdmin(
        title="FastAdmin",
        description="A fast admin dashboard based on fastapi and tortoise-orm with tabler ui.",
    )
    app.add_middleware(BaseHTTPMiddleware, dispatch=middlewares.language_processor)
    app.include_router(router)
    return app


@pytest.mark.asyncio
async def test_configure(fastapi_admin_app, mock_redis):
    app = fastapi_admin_app
    if not hasattr(app, 'redis'):
        app.redis = None
    assert app.redis is None
    await app.configure(redis=mock_redis, logo_url="http://example.com/logo.png")
    assert app.redis == mock_redis
    assert app.logo_url == "http://example.com/logo.png"


@pytest.mark.asyncio
async def test_register_providers(fastapi_admin_app):
    class MockProvider(Provider):
        name = "mock_provider"

    app = fastapi_admin_app
    provider = MockProvider()
    await app._register_providers([provider])
    assert hasattr(app, 'mock_provider')


@pytest.mark.asyncio
async def test_register_resources(fastapi_admin_app):
    class MockResource(Resource):
        label = "Mock Resource"

    app = fastapi_admin_app
    app.register_resources(MockResource)
    assert MockResource in app.resources


@pytest.mark.asyncio
async def test_set_model_resource(fastapi_admin_app):
    class MockModel(Model):
        pass

    class MockModelResource(ModelResource):
        model = MockModel

    app = fastapi_admin_app
    app._set_model_resource(MockModelResource)
    assert MockModel in app.model_resources
    assert app.model_resources[MockModel] == MockModelResource


@pytest.mark.asyncio
async def test_get_model_resource(fastapi_admin_app):
    class MockModel(Model):
        pass

    class MockModelResource(ModelResource):
        model = MockModel

    app = fastapi_admin_app
    app.model_resources[MockModel] = MockModelResource
    resource = app.get_model_resource(MockModel)
    assert isinstance(resource, MockModelResource)


@pytest.mark.asyncio
async def test_get_model_resource_non_existing(fastapi_admin_app):
    class MockModel(Model):
        pass

    app = fastapi_admin_app
    resource = app.get_model_resource(MockModel)
    assert resource is None
