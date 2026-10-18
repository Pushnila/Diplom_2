import uuid

import allure
import requests

from data import REQUEST_TIMEOUT
from urls import Urls


@allure.step('Сгенерировать уникальные данные пользователя')
def generate_user_data():
    unique_value = uuid.uuid4().hex[:12]

    return {
        'email': f'vladislav_{unique_value}@ya.ru',
        'password': f'password_{unique_value}',
        'name': 'Владислав',
    }


@allure.step('Создать пользователя')
def create_user(user_data):
    return requests.post(
        Urls.REGISTER_USER,
        json=user_data,
        timeout=REQUEST_TIMEOUT,
    )


@allure.step('Войти под пользователем')
def login_user(user_data):
    return requests.post(
        Urls.LOGIN_USER,
        json=user_data,
        timeout=REQUEST_TIMEOUT,
    )


@allure.step('Удалить пользователя')
def delete_user(access_token):
    return requests.delete(
        Urls.USER_PROFILE,
        headers={'Authorization': access_token},
        timeout=REQUEST_TIMEOUT,
    )


@allure.step('Получить список ингредиентов')
def get_ingredients():
    return requests.get(
        Urls.INGREDIENTS,
        timeout=REQUEST_TIMEOUT,
    )


@allure.step('Получить идентификаторы ингредиентов')
def get_ingredient_ids():
    response = get_ingredients()

    return [ingredient['_id'] for ingredient in response.json()['data'][:2]]


@allure.step('Создать заказ')
def create_order(ingredients, access_token=None):
    headers = {'Authorization': access_token} if access_token else None

    return requests.post(
        Urls.CREATE_ORDER,
        json={'ingredients': ingredients},
        headers=headers,
        timeout=REQUEST_TIMEOUT,
    )
