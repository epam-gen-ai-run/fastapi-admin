import pytest
from starlette.testclient import TestClient
from fastapi import FastAPI
from fastapi_admin.middlewares import language_processor


@pytest.fixture
def app():
    app = FastAPI()
    app.middleware("http")(language_processor)

    @app.get("/")
    async def read_root():
        return {"message": "Hello World"}

    return app


@pytest.fixture
def client(app):
    return TestClient(app)


def test_language_query_param(client):
    response = client.get("/?language=fr")
    assert response.status_code == 200
    assert response.cookies.get("language") == "fr"


def test_language_cookie(client):
    client.cookies.set("language", "es")
    response = client.get("/")
    assert response.status_code == 200
    assert response.cookies.get("language") == "es"


def test_accept_language_header(client):
    response = client.get("/", headers={"Accept-Language": "fr-FR,fr;q=0.9"})
    assert response.status_code == 200
    assert response.cookies.get("language") == "fr_FR"


def test_no_language(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.cookies.get("language") is None