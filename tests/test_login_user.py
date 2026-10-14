import allure
import pytest
import requests

from data import REQUEST_TIMEOUT
from urls import Urls


@allure.epic('Stellar Burgers API')
@allure.feature('Логин пользователя')
class TestLoginUser:

    @allure.title('Существующий пользователь может войти')
    def test_login_existing_user_success(self, registered_user):
        response = requests.post(
            Urls.LOGIN_USER,
            json=registered_user['user_data'],
            timeout=REQUEST_TIMEOUT
        )

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'accessToken' in response.json()

    @allure.title('Нельзя войти с неверным полем: {field}')
    @pytest.mark.parametrize(
        'field, wrong_value',
        [
            ('email', 'wrong_email@ya.ru'),
            ('password', 'wrong_password'),
        ],
        ids=['wrong-email', 'wrong-password']
    )
    def test_login_with_wrong_credentials_returns_error(
        self,
        registered_user,
        field,
        wrong_value
    ):
        login_data = registered_user['user_data'].copy()
        login_data[field] = wrong_value

        response = requests.post(
            Urls.LOGIN_USER,
            json=login_data,
            timeout=REQUEST_TIMEOUT
        )

        assert response.status_code == 401
        assert response.json()['success'] is False
        assert (
            response.json()['message']
            == 'email or password are incorrect'
        )
