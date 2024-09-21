import os


def get_client_code():
    return os.environ.get('Auth.userid')


def get_password():
    return os.environ.get('Auth.password')


def get_auth():
    client_code = get_client_code()
    password = get_password()
    return {
        'client_code': client_code,
        'password': password,
    }
