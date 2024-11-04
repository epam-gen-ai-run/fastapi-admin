import pytest
from fastapi import HTTPException
from starlette.requests import Request
from starlette.testclient import TestClient
from fastapi_admin.exceptions import (
    ServerHTTPException, InvalidResource, NoSuchFieldFound, FileMaxSizeLimit, FileExtNotAllowed,
    server_error_exception, not_found_error_exception, forbidden_error_exception, unauthorized_error_exception
)
from fastapi_admin.template import templates


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
