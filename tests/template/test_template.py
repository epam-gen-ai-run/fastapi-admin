import pytest
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from fastapi_admin.template import current_page_with_params, set_global_env, add_template_folder, templates
from unittest.mock import Mock

# Test current_page_with_params
def test_current_page_with_params():
    request = Mock(spec=Request)
    request.scope = {"raw_path": b"/test_path"}
    request.query_params = {"param1": "value1"}
    context = {"request": request}
    params = {"param2": "value2"}
    expected_result = "/test_path?param1=value1&param2=value2"
    result = current_page_with_params(context, params)
    assert result == expected_result

# Test set_global_env
def test_set_global_env():
    set_global_env("TEST_ENV", "test_value")
    assert templates.env.globals["TEST_ENV"] == "test_value"

# Test add_template_folder
def test_add_template_folder():
    folder_path = "./new_template_folder"
    add_template_folder(folder_path)
    assert folder_path in templates.env.loader.searchpath
