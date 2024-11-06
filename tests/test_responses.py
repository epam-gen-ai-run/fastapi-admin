import pytest
from starlette.testclient import TestClient
from starlette.requests import Request
from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse
from starlette.routing import NoMatchFound
from fastapi_admin.responses import redirect

app = FastAPI()

# Set up admin_path in the FastAPI app
app.admin_path = "/admin"

router = APIRouter()

@router.get("/test-view", name="test-view")
def test_view():
    return {"message": "This is a test view."}

app.include_router(router)


def test_view_registration():
    client = TestClient(app)
    response = client.get("/test-view")
    assert response.status_code == 200
    assert response.json() == {"message": "This is a test view."}


@pytest.mark.asyncio
async def test_redirect_with_params():
    async def mock_request_scope(app):
        return Request(scope={
            "type": "http",
            "app": app,
            "path": "/dummy",
            "headers": {},
        })

    request = await mock_request_scope(app)
    response = redirect(request, "test-view")
    assert response.status_code == 303
    assert response.headers["location"] == "/admin/test-view"


@pytest.mark.asyncio
async def test_redirect_without_params():
    async def mock_request_scope(app):
        return Request(scope={
            "type": "http",
            "app": app,
            "path": "/dummy",
            "headers": {},
        })

    request = await mock_request_scope(app)
    response = redirect(request, "test-view")
    assert response.status_code == 303
    assert response.headers["location"] == "/admin/test-view"


@pytest.mark.asyncio
async def test_redirect_invalid_view():
    async def mock_request_scope(app):
        return Request(scope={
            "type": "http",
            "app": app,
            "path": "/dummy",
            "headers": {},
        })

    request = await mock_request_scope(app)
    try:
        response = redirect(request, "invalid-view")
    except Exception as e:
        assert isinstance(e, NoMatchFound)


@pytest.mark.asyncio
async def test_redirect_special_characters_in_params():
    async def mock_request_scope(app):
        return Request(scope={
            "type": "http",
            "app": app,
            "path": "/dummy",
            "headers": {},
        })

    request = await mock_request_scope(app)
    response = redirect(request, "test-view")
    assert response.status_code == 303
    assert response.headers["location"] == "/admin/test-view"
