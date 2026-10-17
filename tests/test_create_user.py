import allure
import pytest

from helpers import create_user, delete_user, generate_user_data


@allure.epic('Stellar Burgers API')
@allure.feature('Создание пользователя')
class TestCreateUser:

    @allure.title('Можно создать уникального пользователя')
    def test_create_unique_user_success(self):
        user_data = generate_user_data()
        response = create_user(user_data)
        response_body = response.json()
        access_token = response_body.get('accessToken')

        try:
            assert response.status_code == 200
            assert response_body['success'] is True
            assert access_token is not None
        finally:
            if access_token:
                delete_user(access_token)

    @allure.title('Нельзя создать пользователя, который уже зарегистрирован')
    def test_create_duplicate_user_returns_error(self, registered_user):
        response = create_user(registered_user['user_data'])

        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == 'User already exists'

    @allure.title('Нельзя создать пользователя без обязательного поля: {field}')
    @pytest.mark.parametrize(
        'field',
        ['email', 'password', 'name'],
        ids=['without-email', 'without-password', 'without-name'],
    )
    def test_create_user_without_required_field_returns_error(self, field):
        user_data = generate_user_data()
        user_data.pop(field)

        response = create_user(user_data)

        assert response.status_code == 403
        assert response.json()['success'] is False
        assert (
            response.json()['message']
            == 'Email, password and name are required fields'
        )
