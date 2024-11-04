import pytest
import bcrypt
from fastapi_admin.utils import generate_random_str, check_password, hash_password


def test_generate_random_str():
    length = 10
    result = generate_random_str(length)
    assert len(result) == length
    assert result.isdigit()

    result = generate_random_str(length, is_digit=False)
    assert len(result) == length
    assert all(c.isalnum() for c in result)


def test_check_password():
    password = "test_password"
    password_hash = hash_password(password)

    assert check_password(password, password_hash) is True
    assert check_password("wrong_password", password_hash) is False


def test_hash_password():
    password = "test_password"
    password_hash = hash_password(password)

    assert bcrypt.checkpw(password.encode(), password_hash.encode())

    # Ensure it works with check_password function
    assert check_password(password, password_hash)