import uuid


def generate_user_data():
    unique_value = uuid.uuid4().hex[:12]

    return {
        'email': f'vladislav_{unique_value}@ya.ru',
        'password': f'password_{unique_value}',
        'name': 'Владислав'
    }
