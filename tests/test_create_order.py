import allure
import requests

from data import INVALID_INGREDIENT_HASH, REQUEST_TIMEOUT
from urls import Urls


@allure.epic('Stellar Burgers API')
@allure.feature('Создание заказа')
class TestCreateOrder:

    @allure.title('Можно создать заказ с авторизацией')
    def test_create_order_with_authorization_success(
        self,
        registered_user,
        ingredient_ids
    ):
        response = requests.post(
            Urls.CREATE_ORDER,
            json={'ingredients': [ingredient_ids[0]]},
            headers={
                'Authorization': registered_user['access_token']
            },
            timeout=REQUEST_TIMEOUT
        )

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'order' in response.json()

    @allure.title('Можно создать заказ без авторизации')
    def test_create_order_without_authorization_success(
        self,
        ingredient_ids
    ):
        response = requests.post(
            Urls.CREATE_ORDER,
            json={'ingredients': [ingredient_ids[0]]},
            timeout=REQUEST_TIMEOUT
        )

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'order' in response.json()

    @allure.title('Можно создать заказ с несколькими ингредиентами')
    def test_create_order_with_several_ingredients_success(
        self,
        ingredient_ids
    ):
        response = requests.post(
            Urls.CREATE_ORDER,
            json={'ingredients': ingredient_ids},
            timeout=REQUEST_TIMEOUT
        )

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'order' in response.json()

    @allure.title('Нельзя создать заказ без ингредиентов')
    def test_create_order_without_ingredients_returns_error(
        self,
        registered_user
    ):
        response = requests.post(
            Urls.CREATE_ORDER,
            json={'ingredients': []},
            headers={
                'Authorization': registered_user['access_token']
            },
            timeout=REQUEST_TIMEOUT
        )

        assert response.status_code == 400
        assert response.json()['success'] is False
        assert (
            response.json()['message']
            == 'Ingredient ids must be provided'
        )

    @allure.title('Нельзя создать заказ с неверным хешем ингредиента')
    def test_create_order_with_invalid_ingredient_hash_returns_error(self):
        response = requests.post(
            Urls.CREATE_ORDER,
            json={'ingredients': [INVALID_INGREDIENT_HASH]},
            timeout=REQUEST_TIMEOUT
        )

        assert response.status_code == 500
