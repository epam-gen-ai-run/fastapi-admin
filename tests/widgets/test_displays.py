import pytest
from unittest.mock import Mock
from datetime import datetime
import json
from starlette.requests import Request
from fastapi_admin.widgets.displays import Display, DatetimeDisplay, DateDisplay, InputOnly, Boolean, Image, Json


# Test Display class
class TestDisplay:
    def test_display_initialization(self):
        widget = Display()
        assert isinstance(widget, Display)


# Test DatetimeDisplay class
class TestDatetimeDisplay:
    def test_datetime_display_initialization(self):
        widget = DatetimeDisplay()
        assert isinstance(widget, DatetimeDisplay)
        assert widget.format_ == '%Y-%m-%d %H:%M:%S'

    @pytest.mark.asyncio
    async def test_datetime_display_render(self):
        widget = DatetimeDisplay('%Y-%m-%d')
        request = Mock(Request)
        value = datetime(2023, 1, 1, 12, 0, 0)
        result = await widget.render(request, value)
        assert result is not None


# Test DateDisplay class
class TestDateDisplay:
    def test_date_display_initialization(self):
        widget = DateDisplay()
        assert isinstance(widget, DateDisplay)
        assert widget.format_ == '%Y-%m-%d'


# Test InputOnly class
class TestInputOnly:
    def test_input_only_initialization(self):
        widget = InputOnly()
        assert isinstance(widget, InputOnly)


# Test Boolean class
class TestBoolean:
    def test_boolean_initialization(self):
        widget = Boolean()
        assert isinstance(widget, Boolean)
        assert widget.template == 'widgets/displays/boolean.html'


# Test Image class
class TestImage:
    def test_image_initialization(self):
        widget = Image()
        assert isinstance(widget, Image)
        assert widget.template == 'widgets/displays/image.html'


# Test Json class
class TestJson:
    def test_json_initialization(self):
        widget = Json()
        assert isinstance(widget, Json)
        assert widget.template == 'widgets/displays/json.html'

    @pytest.mark.asyncio
    async def test_json_render(self, mocker):
        widget = Json()
        request = Mock(Request)
        value = {'key': 'value'}
        
        # Mock the super().render method
        mock_render = mocker.patch.object(Display, 'render', return_value=json.dumps(value))
        
        result = await widget.render(request, value)
        assert result is not None
        mock_render.assert_called_once_with(request, json.dumps(value))
        assert json.loads(result) == value
