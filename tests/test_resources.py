import pytest
from fastapi_admin.resources import *
from starlette.requests import Request
from tortoise import Tortoise, fields, models
from pydantic import BaseModel

class MockRequest(Request):
    def __init__(self):
        pass

class MockModel(TortoiseModel):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)


@pytest.mark.asyncio
async def test_resource():
    resource = Resource()
    resource.label = None
    resource.icon = ""
    assert resource.label is None
    assert resource.icon == ""


@pytest.mark.asyncio
async def test_link():
    link = Link()
    link.label = None
    link.icon = ""
    link.url = None
    link.target = "_self"
    assert link.label is None
    assert link.icon == ""
    assert link.url is None
    assert link.target == "_self"


@pytest.mark.asyncio
async def test_field():
    field = Field(name="test")
    assert field.name == "test"
    assert field.label == "Test"
    assert isinstance(field.display, displays.Display)
    assert isinstance(field.input, inputs.Input)

@pytest.mark.asyncio
async def test_computefield():
    field = ComputeField(name="test")
    value = await field.get_value(MockRequest(), {"test": "value"})
    assert value == "value"


@pytest.mark.asyncio
async def test_action():
    action = Action(icon="test", label="Test", name="test")
    assert action.icon == "test"
    assert action.label == "Test"
    assert action.name == "test"
    assert action.method == Method.POST
    assert action.ajax is True

@pytest.mark.asyncio
async def test_toolbar_action():
    action = ToolbarAction(icon="test", label="Test", name="test", class_=None)
    assert action.class_ is None

@pytest.mark.asyncio
async def test_model():
    model = Model()
    model.label = None
    model.icon = ""
    model.page_size = 10
    model.page_pre_title = None
    model.page_title = None
    model.fields = []
    model.filters = []
    assert model.label is None
    assert model.icon == ""
    assert model.page_size == 10
    assert model.page_pre_title is None
    assert model.page_title is None
    assert model.fields == []
    assert model.filters == []

@pytest.mark.asyncio
async def test_dropdown():
    dropdown = Dropdown()
    dropdown.label = None
    dropdown.icon = ""
    dropdown.resources = []
    assert dropdown.label is None
    assert dropdown.icon == ""
    assert dropdown.resources == []

@pytest.mark.asyncio
async def test_render_values():
    model = Model()
    fields = [Field(name="test")]
    values = [{"test": "value"}]
    result = await render_values(MockRequest(), model, fields, values)
    assert result is not None