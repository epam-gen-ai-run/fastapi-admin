import pytest
from datetime import datetime
from starlette.requests import Request
from fastapi_admin.widgets.displays import (
    Display, DatetimeDisplay, DateDisplay, InputOnly, Boolean, Json
)

# Mock request object
class MockRequest(Request):
    def __init__(self):
        pass

@pytest.mark.asyncio
async def test_display_initialization():
    display = Display()
    assert isinstance(display, Display)

@pytest.mark.asyncio
async def test_datetime_display_initialization_default_format():
    datetime_display = DatetimeDisplay()
    assert datetime_display.format_ == '%Y-%m-%d %H:%M:%S'

@pytest.mark.asyncio
async def test_datetime_display_initialization_custom_format():
    custom_format = '%d-%m-%Y %H:%M:%S'
    datetime_display = DatetimeDisplay(format_=custom_format)
    assert datetime_display.format_ == custom_format

@pytest.mark.asyncio
async def test_datetime_display_render_valid_datetime():
    datetime_display = DatetimeDisplay()
    mock_request = MockRequest()
    value = datetime(2023, 10, 5, 15, 30, 45)
    result = await datetime_display.render(mock_request, value)
    assert result == '2023-10-05 15:30:45'

@pytest.mark.asyncio
async def test_datetime_display_render_none_value():
    datetime_display = DatetimeDisplay()
    mock_request = MockRequest()
    result = await datetime_display.render(mock_request, None)
    assert result == ''

@pytest.mark.asyncio
async def test_date_display_initialization_default_format():
    date_display = DateDisplay()
    assert date_display.format_ == '%Y-%m-%d'

@pytest.mark.asyncio
async def test_date_display_initialization_custom_format():
    custom_format = '%d-%m-%Y'
    date_display = DateDisplay(format_=custom_format)
    assert date_display.format_ == custom_format

@pytest.mark.asyncio
async def test_input_only_initialization():
    input_only = InputOnly()
    assert isinstance(input_only, InputOnly)

@pytest.mark.asyncio
async def test_boolean_initialization():
    boolean = Boolean()
    assert boolean.template == 'widgets/displays/boolean.html'

@pytest.mark.asyncio
async def test_json_initialization():
    json_display = Json()
    assert json_display.template == 'widgets/displays/json.html'

@pytest.mark.asyncio
async def test_json_render_empty_dict():
    json_display = Json()
    mock_request = MockRequest()
    value = {}
    result = await json_display.render(mock_request, value)
    expected_result = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@10.7.2/build/styles/default.min.css">\n'
    expected_result += '<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@10.7.2/build/highlight.min.js"></script>\n'
    expected_result += '<script>hljs.highlightAll();</script>\n'
    expected_result += '<pre><code class="json">{}</code></pre>'
    assert result == expected_result

@pytest.mark.asyncio
async def test_json_render_none_value():
    json_display = Json()
    mock_request = MockRequest()
    result = await json_display.render(mock_request, None)
    expected_result = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@10.7.2/build/styles/default.min.css">\n'
    expected_result += '<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@10.7.2/build/highlight.min.js"></script>\n'
    expected_result += '<script>hljs.highlightAll();</script>\n'
    expected_result += '<pre><code class="json">null</code></pre>'
    assert result == expected_result
