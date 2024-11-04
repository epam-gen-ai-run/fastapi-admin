import pytest
from fastapi_admin.enums import Method, StrEnum


def test_str_enum():
    class TestEnum(StrEnum):
        TEST = 'test'

    assert str(TestEnum.TEST) == 'test'


def test_method_enum():
    assert Method.GET == 'GET'
    assert Method.POST == 'POST'
    assert Method.DELETE == 'DELETE'
    assert Method.PUT == 'PUT'
    assert Method.PATCH == 'PATCH'
