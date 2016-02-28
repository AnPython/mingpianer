# coding:utf-8

from django.conf import settings

from .models import Philosopherstone


def profile_temporary_url(openid):
    stone = Philosopherstone.objects.get_or_create(openid)[0]
    url = '{host}/{profile_name}/{code}'.format(settings.MY_HOST, settings.MY_PROFILE_NAME, stone.code)
    return url
