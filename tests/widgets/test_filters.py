import pytest
from starlette.requests import Request
from fastapi_admin.widgets.filters import Filter, Search, Datetime, Date, Select, Enum, Boolean
import pendulum
from enum import Enum as EnumCLS

@pytest.fixture
def mock_request():
    return Request(scope={"type": "http"})

@pytest.mark.asyncio
async def test_search_init():
    search_widget = Search(name="test", label="Test", search_mode="contains")
    assert search_widget.context["search_mode"] == "contains"

@pytest.mark.asyncio
async def test_datetime_parse_value(mock_request):
    datetime_widget = Datetime(name="test", label="Test")
    value = "2021-01-01 00:00:00 - 2021-01-02 00:00:00"
    result = await datetime_widget.parse_value(mock_request, value)
    assert result == (pendulum.parse("2021-01-01 00:00:00"), pendulum.parse("2021-01-02 00:00:00"))

@pytest.mark.asyncio
async def test_date_init():
    date_widget = Date(name="test", label="Test")
    assert date_widget.context["date"] is True

@pytest.mark.asyncio
async def test_select_get_options():
    class TestSelect(Select):
        async def get_options(self):
            return [("option1", 1), ("option2", 2)]
    select_widget = TestSelect(name="test", label="Test")
    options = await select_widget.get_options()
    assert options == [("option1", 1), ("option2", 2)]

@pytest.mark.asyncio
async def test_enum_parse_value(mock_request):
    class TestEnum(EnumCLS):
        OPTION1 = 1
        OPTION2 = 2
    enum_widget = Enum(enum=TestEnum, name="test", label="Test")
    result = await enum_widget.parse_value(mock_request, 1)
    assert result == TestEnum.OPTION1
