import allure
import pytest
import requests

from data import REQUEST_TIMEOUT
from urls import Urls


@allure.epic('Stellar Burgers API')
@allure.feature('Создание пользователя')
class TestCreateUser:

    @allure.title('Можно создать уникального пользователя')
    def test_create_unique_user_success(
        self,
        user_data,
        user_tokens_for_cleanup
    ):
        response = requests.post(
            Urls.REGISTER_USER,
            json=user_data,
            timeout=REQUEST_TIMEOUT
        )
        response_body = response.json()
        access_token = response_body.get('accessToken')

        if access_token:
            user_tokens_for_cleanup.append(access_token)

        assert response.status_code == 200
        assert response_body['success'] is True
        assert access_token is not None

    @allure.title('Нельзя создать пользователя, который уже зарегистрирован')
    def test_create_duplicate_user_returns_error(self, registered_user):
        response = requests.post(
            Urls.REGISTER_USER,
            json=registered_user['user_data'],
            timeout=REQUEST_TIMEOUT
        )

        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == 'User already exists'

    @allure.title('Нельзя создать пользователя без обязательного поля: {field}')
    @pytest.mark.parametrize(
        'field',
        ['email', 'password', 'name'],
        ids=['without-email', 'without-password', 'without-name']
    )
    def test_create_user_without_required_field_returns_error(
        self,
        user_data,
        field
    ):
        user_data.pop(field)

        response = requests.post(
            Urls.REGISTER_USER,
            json=user_data,
            timeout=REQUEST_TIMEOUT
        )

        assert response.status_code == 403
        assert response.json()['success'] is False
        assert (
            response.json()['message']
            == 'Email, password and name are required fields'
        )
