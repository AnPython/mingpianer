# coding:utf-8

import random

from django.conf import settings

from .models import Philosopherstone, Mingpian


def profile_temporary_url(openid):
    mingpian = Mingpian.objects.get_or_create(openid=openid)[0]
    stone = Philosopherstone.objects.create(player=mingpian)
    url = '{host}/{profile_name}/{code}'.format(host=settings.MY_HOST,
                                                 profile_name=settings.MY_PROFILE_NAME,
                                                 code=stone.code)
    return url


def generate_code():
    code_len = 10
    raw_words = 'abcdefghijklmnopqrstuvwxyz0123456789'
    _code = ''
    for i in range(code_len):
        random_num = random.randint(0, len(raw_words) - 1)
        _code += raw_words[random_num]
    return _code
