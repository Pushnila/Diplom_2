import pytest
import requests

from data import REQUEST_TIMEOUT
from helpers import generate_user_data
from urls import Urls


@pytest.fixture
def user_data():
    return generate_user_data()


@pytest.fixture
def registered_user(user_data):
    response = requests.post(
        Urls.REGISTER_USER,
        json=user_data,
        timeout=REQUEST_TIMEOUT
    )
    assert response.status_code == 200, response.text

    access_token = response.json()['accessToken']

    yield {
        'user_data': user_data,
        'access_token': access_token
    }

    requests.delete(
        Urls.USER_PROFILE,
        headers={'Authorization': access_token},
        timeout=REQUEST_TIMEOUT
    )


@pytest.fixture
def user_tokens_for_cleanup():
    tokens = []

    yield tokens

    for token in tokens:
        requests.delete(
            Urls.USER_PROFILE,
            headers={'Authorization': token},
            timeout=REQUEST_TIMEOUT
        )


@pytest.fixture
def ingredient_ids():
    response = requests.get(
        Urls.INGREDIENTS,
        timeout=REQUEST_TIMEOUT
    )
    assert response.status_code == 200, response.text

    return [
        ingredient['_id']
        for ingredient in response.json()['data'][:2]
    ]
