import pytest
from unittest.mock import AsyncMock, Mock, patch
from fastapi import FastAPI, Request, Form, Depends
from starlette.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from tortoise import fields, Tortoise
from tortoise.models import Model
from tortoise.contrib.test import finalizer, initializer
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin.models import AbstractAdmin
from fastapi_admin.utils import hash_password, check_password
from fastapi_admin.template import templates
from fastapi_admin.depends import get_redis, get_current_admin, get_resources

class MockAdmin(AbstractAdmin):
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=200)

@pytest.fixture(scope='module', autouse=True)
async def init_db():
    await Tortoise.init(config={
        'connections': {'default': 'sqlite://:memory:'},
        'apps': {'models': {'models': ['__main__'], 'default_connection': 'default'}}
    })
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()
    finalizer()

@pytest.fixture
async def provider():
    return UsernamePasswordProvider(admin_model=MockAdmin)

@pytest.mark.asyncio
async def test_login_view(provider):
    provider = await provider
    request = Mock(Request)
    request.app.admin_path = "/admin"
    response = await provider.login_view(request)
    assert response.template.name == "providers/login/login.html"
    assert "request" in response.context

@pytest.mark.asyncio
async def test_register(provider):
    provider = await provider
    app = FastAPI()
    await provider.register(app)
    assert app.routes

@pytest.mark.asyncio
async def test_pre_save_admin(provider):
    provider = await provider
    instance = MockAdmin(username="admin", password="new_password")
    await provider.pre_save_admin(None, instance, None, None)
    assert instance.password != "new_password"



@pytest.mark.asyncio
async def test_logout(provider):
    provider = await provider
    request = Mock(Request)
    request.cookies = {provider.access_token: "token"}
    request.app.admin_path = "/admin"
    request.app.redis = AsyncMock()
    response = await provider.logout(request)
    assert isinstance(response, RedirectResponse)

@pytest.mark.asyncio
async def test_redirect_login(provider):
    provider = await provider
    request = Mock(Request)
    request.app.admin_path = "/admin"
    response = provider.redirect_login(request)
    assert isinstance(response, RedirectResponse)

@pytest.mark.asyncio
async def test_password_view(provider):
    provider = await provider
    request = Mock(Request)
    request.app.admin_path = "/admin"
    request.scope = {"path": "/password", "raw_path": b"/password"}
    request.state.admin = MockAdmin(username="admin", password=hash_password("123"))
    request.cookies = {}
    request.query_params = {}
    response = await provider.password_view(request, resources=[])  # Mock resources dependency
    assert response.template.name == "providers/login/password.html"

