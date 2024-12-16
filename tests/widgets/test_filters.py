import pytest
from starlette.requests import Request
from fastapi_admin.widgets.filters import Filter, Search, Datetime, Date, Select, Enum, Boolean, ForeignKey, DistinctColumn
import pendulum
from enum import Enum as EnumCLS
from tortoise import Model, Tortoise
from tortoise.queryset import QuerySet

@pytest.fixture
def mock_request():
    return Request(scope={"type": "http"})

@pytest.fixture(scope="module", autouse=True)
async def init_db():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

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

@pytest.mark.asyncio
async def test_boolean_get_options():
    boolean_widget = Boolean(name="test", label="Test")
    options = await boolean_widget.get_options()
    assert options == [("", ""), ("TRUE", "true"), ("FALSE", "false")]

@pytest.mark.asyncio
async def test_filter_init():
    filter_widget = Filter(name="test", label="Test")
    assert filter_widget.context["name"] == "test"
    assert filter_widget.context["label"] == "Test"

@pytest.mark.asyncio
async def test_search_different_modes():
    modes = ["equal", "contains", "icontains", "startswith", "istartswith", "endswith", "iendswith", "iexact", "search"]
    for mode in modes:
        search_widget = Search(name="test", label="Test", search_mode=mode)
        if mode == "equal":
            assert search_widget.context["name"] == "test"
        else:
            assert search_widget.context["name"] == f"test__{mode}"

@pytest.mark.asyncio
async def test_datetime_render(mock_request):
    datetime_widget = Datetime(name="test", label="Test")
    value = (pendulum.parse("2021-01-01 00:00:00"), pendulum.parse("2021-01-02 00:00:00"))
    rendered = await datetime_widget.render(mock_request, value)
    assert "2021-01-01" in rendered
    assert "2021-01-02" in rendered

@pytest.mark.asyncio
async def test_select_render(mock_request):
    class TestSelect(Select):
        async def get_options(self):
            return [("option1", 1), ("option2", 2)]
    select_widget = TestSelect(name="test", label="Test")
    rendered = await select_widget.render(mock_request, 1)
    assert "option1" in rendered
    assert "option2" in rendered

@pytest.mark.asyncio
async def test_foreign_key_init():
    class TestModel(Model):
        pass
    fk_widget = ForeignKey(model=TestModel, name="test", label="Test")
    assert fk_widget.context["name"] == "test"
    assert fk_widget.context["label"] == "Test"

@pytest.mark.asyncio
async def test_foreign_key_get_options(mock_request):
    class TestModel(Model):
        @classmethod
        async def all(cls):
            return [cls()]
    fk_widget = ForeignKey(model=TestModel, name="test", label="Test")
    options = await fk_widget.get_options()
    assert len(options) > 0

@pytest.mark.asyncio
async def test_foreign_key_get_models(mock_request):
    class TestModel(Model):
        @classmethod
        async def all(cls):
            return [cls()]
    fk_widget = ForeignKey(model=TestModel, name="test", label="Test")
    models = await fk_widget.get_models()
    assert len(models) > 0

@pytest.mark.asyncio
async def test_foreign_key_render(mock_request):
    class TestModel(Model):
        @classmethod
        async def all(cls):
            return [cls()]
    fk_widget = ForeignKey(model=TestModel, name="test", label="Test")
    rendered = await fk_widget.render(mock_request, 1)
    assert "None" in rendered

@pytest.mark.asyncio
async def test_distinct_column_init():
    class TestModel(Model):
        pass
    dc_widget = DistinctColumn(model=TestModel, name="test", label="Test")
    assert dc_widget.context["name"] == "test"
    assert dc_widget.context["label"] == "Test"

