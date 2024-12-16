import pytest
from starlette.datastructures import UploadFile
from starlette.requests import Request
from tortoise import Model
from fastapi_admin.file_upload import FileUpload
from fastapi_admin.widgets.inputs import (
    Input, DisplayOnly, Text, Select, ForeignKey, ManyToMany, Enum, 
    Email, Json, TextArea, Editor, DateTime, Date, File, Image, 
    Radio, RadioEnum, Switch, Password, Number, Color
)
from enum import Enum as EnumCLS

class MockModel(Model):
    pk = 1
    related_objects = []

    @classmethod
    async def all(cls):
        return [cls()]

class MockFileUpload(FileUpload):
    async def upload(self, file: UploadFile):
        return "mock_url"

@pytest.fixture
def mock_request():
    return Request(scope={"type": "http"})

@pytest.mark.asyncio
async def test_input_render(mock_request):
    input_widget = Input()
    result = await input_widget.render(mock_request, "test")
    assert "test" in result

@pytest.mark.asyncio
async def test_text_render(mock_request):
    text_widget = Text()
    result = await text_widget.render(mock_request, "test")
    assert "test" in result

@pytest.mark.asyncio
async def test_select_render(mock_request):
    class TestSelect(Select):
        async def get_options(self):
            return [("option1", 1), ("option2", 2)]
    select_widget = TestSelect()
    select_widget.context['name'] = 'test'
    result = await select_widget.render(mock_request, 1)
    assert "option1" in result

@pytest.mark.asyncio
async def test_foreign_key_render(mock_request):
    foreign_key_widget = ForeignKey(MockModel)
    foreign_key_widget.context['name'] = 'test'
    result = await foreign_key_widget.render(mock_request, MockModel())
    assert "1" in result

@pytest.mark.asyncio
async def test_many_to_many_render(mock_request):
    many_to_many_widget = ManyToMany(MockModel)
    many_to_many_widget.context['name'] = 'test'
    result = await many_to_many_widget.render(mock_request, MockModel())
    assert "1" in result

@pytest.mark.asyncio
async def test_enum_render(mock_request):
    class TestEnum(EnumCLS):
        OPTION1 = 1
        OPTION2 = 2
    enum_widget = Enum(TestEnum)
    enum_widget.context['name'] = 'test'
    result = await enum_widget.render(mock_request, TestEnum.OPTION1)
    assert "OPTION1" in result

@pytest.mark.asyncio
async def test_file_render(mock_request):
    file_widget = File(MockFileUpload("uploads_dir"))
    result = await file_widget.render(mock_request, "test")
    assert "test" in result

@pytest.mark.asyncio
async def test_image_render(mock_request):
    image_widget = Image(MockFileUpload("uploads_dir"))
    result = await image_widget.render(mock_request, "test")
    assert "test" in result

@pytest.mark.asyncio
async def test_radio_render(mock_request):
    radio_widget = Radio([("option1", 1), ("option2", 2)])
    result = await radio_widget.render(mock_request, 1)
    assert "option1" in result

@pytest.mark.asyncio
async def test_radio_enum_render(mock_request):
    class TestEnum(EnumCLS):
        OPTION1 = 1
        OPTION2 = 2
    radio_enum_widget = RadioEnum(TestEnum)
    radio_enum_widget.context['name'] = 'test'
    result = await radio_enum_widget.render(mock_request, TestEnum.OPTION1)
    assert "OPTION1" in result

@pytest.mark.asyncio
async def test_switch_render(mock_request):
    switch_widget = Switch()
    result = await switch_widget.render(mock_request, "on")
    assert "checked" in result

@pytest.mark.asyncio
async def test_password_render(mock_request):
    password_widget = Password()
    result = await password_widget.render(mock_request, "test")
    assert "test" in result

@pytest.mark.asyncio
async def test_number_render(mock_request):
    number_widget = Number()
    result = await number_widget.render(mock_request, "123")
    assert "123" in result

@pytest.mark.asyncio
async def test_color_render(mock_request):
    color_widget = Color()
    result = await color_widget.render(mock_request, "#FFFFFF")
    assert "#FFFFFF" in result
