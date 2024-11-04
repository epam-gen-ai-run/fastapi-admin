import pytest
from starlette.testclient import TestClient
from starlette.requests import Request
from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse
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
