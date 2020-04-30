import json
from django.core.exceptions import ImproperlyConfigured


def get_file():
    """ 비밀 변수들을 가져고있는 file 가져오기"""
    with open('./config/secrets.json') as f:
        secrets = json.loads(f.read())
    return secrets


def get_secret(setting, secrets):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)
