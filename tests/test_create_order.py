import allure

from data import INVALID_INGREDIENT_HASH
from helpers import create_order, get_ingredient_ids


@allure.epic('Stellar Burgers API')
@allure.feature('Создание заказа')
class TestCreateOrder:

    @allure.title('Можно создать заказ с авторизацией')
    def test_create_order_with_authorization_success(self, registered_user):
        ingredient_ids = get_ingredient_ids()
        response = create_order(
            [ingredient_ids[0]],
            registered_user['access_token'],
        )

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'order' in response.json()

    @allure.title('Можно создать заказ без авторизации')
    def test_create_order_without_authorization_success(self):
        ingredient_ids = get_ingredient_ids()
        response = create_order([ingredient_ids[0]])

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'order' in response.json()

    @allure.title('Можно создать заказ с несколькими ингредиентами')
    def test_create_order_with_several_ingredients_success(self):
        ingredient_ids = get_ingredient_ids()
        response = create_order(ingredient_ids)

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'order' in response.json()

    @allure.title('Нельзя создать заказ без ингредиентов')
    def test_create_order_without_ingredients_returns_error(self, registered_user):
        response = create_order([], registered_user['access_token'])

        assert response.status_code == 400
        assert response.json()['success'] is False
        assert response.json()['message'] == 'Ingredient ids must be provided'

    @allure.title('Нельзя создать заказ с неверным хешем ингредиента')
    def test_create_order_with_invalid_ingredient_hash_returns_error(self):
        response = create_order([INVALID_INGREDIENT_HASH])

        assert response.status_code == 500
