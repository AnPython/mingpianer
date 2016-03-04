# coding:utf-8

import random
from redis import StrictRedis

from django.conf import settings


redis = StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD)


def generate_code():
    code_len = 10
    raw_words = 'abcdefghijklmnopqrstuvwxyz0123456789'
    _code = ''
    for i in range(code_len):
        random_num = random.randint(0, len(raw_words) - 1)
        _code += raw_words[random_num]
    return _code
