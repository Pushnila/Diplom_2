import pytest

from helpers import create_user, delete_user, generate_user_data


@pytest.fixture
def registered_user():
    user_data = generate_user_data()
    response = create_user(user_data)
    access_token = response.json().get('accessToken')

    yield {
        'user_data': user_data,
        'access_token': access_token,
    }

    if access_token:
        delete_user(access_token)


@pytest.fixture
def access_tokens_for_cleanup():
    access_tokens = []

    yield access_tokens

    for access_token in access_tokens:
        delete_user(access_token)
