import pytest
from app.helpers import check_password, encrypt_password


@pytest.mark.parametrize('sent', [
    ('test'),
    ('changeme'),
    ('1234123'),
])
def test_if_check_password_and_encrypt_password_works_properly(sent):
    expected = encrypt_password(sent)
    assert check_password(sent, expected)
