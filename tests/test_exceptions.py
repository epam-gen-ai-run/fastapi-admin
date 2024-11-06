import pytest
from fastapi import HTTPException
from starlette.requests import Request
from starlette.testclient import TestClient
from fastapi import FastAPI
from fastapi_admin.exceptions import (
    ServerHTTPException, InvalidResource, NoSuchFieldFound, FileMaxSizeLimit, FileExtNotAllowed,
    server_error_exception, not_found_error_exception, forbidden_error_exception, unauthorized_error_exception
)
from fastapi_admin.template import templates

app = FastAPI()


@app.exception_handler(ServerHTTPException)
async def server_error_exception_handler(request: Request, exc: ServerHTTPException):
    return await server_error_exception(request, exc)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return await not_found_error_exception(request, exc)
    elif exc.status_code == 403:
        return await forbidden_error_exception(request, exc)
    elif exc.status_code == 401:
        return await unauthorized_error_exception(request, exc)
    return await server_error_exception(request, exc)


@app.get("/server_error")
async def get_server_error():
    raise ServerHTTPException("Server Error")


@app.get("/not_found")
async def get_not_found():
    raise HTTPException(status_code=404, detail="Page Not Found")


@app.get("/forbidden")
async def get_forbidden():
    raise HTTPException(status_code=403, detail="Access Forbidden")


@app.get("/unauthorized")
async def get_unauthorized():
    raise HTTPException(status_code=401, detail="Unauthorized Access")


def test_server_http_exception():
    exc = ServerHTTPException("Server Error")
    assert exc.status_code == 500
    assert exc.detail == "Server Error"


def test_invalid_resource():
    exc = InvalidResource("Invalid Resource")
    assert exc.status_code == 500
    assert exc.detail == "Invalid Resource"


def test_no_such_field_found():
    exc = NoSuchFieldFound("No Such Field")
    assert exc.status_code == 500
    assert exc.detail == "No Such Field"


def test_file_max_size_limit():
    exc = FileMaxSizeLimit("File Too Large")
    assert exc.status_code == 500
    assert exc.detail == "File Too Large"


def test_file_ext_not_allowed():
    exc = FileExtNotAllowed("Extension Not Allowed")
    assert exc.status_code == 500
    assert exc.detail == "Extension Not Allowed"


def test_server_error_exception():
    client = TestClient(app)
    response = client.get("/server_error")
    assert response.status_code == 500
    assert "500" in response.text
    assert "Oops… You just found an error page" in response.text


def test_not_found_error_exception():
    client = TestClient(app)
    response = client.get("/not_found")
    assert response.status_code == 404
    assert "404" in response.text
    assert "Oops… You just found an error page" in response.text


def test_forbidden_error_exception():
    client = TestClient(app)
    response = client.get("/forbidden")
    assert response.status_code == 403
    assert "403" in response.text
    assert "Oops… You are forbidden" in response.text


def test_unauthorized_error_exception():
    client = TestClient(app)
    response = client.get("/unauthorized")
    assert response.status_code == 401
    assert "401" in response.text
    assert "Oops… You are unauthorized" in response.text
