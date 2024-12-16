import pytest
from tortoise import Tortoise, fields
from tortoise.models import Model


class AbstractAdmin(Model):
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=200)

    class Meta:
        abstract = True


@pytest.fixture(scope='module')
def init_db():
    config = {
        'connections': {'default': 'sqlite://:memory:'},
        'apps': {
            'models': {
                'models': ['__main__'],
                'default_connection': 'default',
            }
        }
    }
    Tortoise.init(config=config)
    Tortoise.generate_schemas()
    yield
    Tortoise.close_connections()


def test_abstract_admin_creation(init_db):
    admin = AbstractAdmin(username='admin', password='password')
    assert admin.username == 'admin'
    assert admin.password == 'password'
