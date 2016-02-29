# coding:utf-8

from django.conf import settings

from .models import Philosopherstone, Mingpian


def profile_temporary_url(openid):
    mingpian = Mingpian.objects.get_or_create(openid=openid)[0]
    stone = Philosopherstone.objects.create(player=mingpian)
    url = '{host}/{profile_name}/{code}'.format(host=settings.MY_HOST,
                                                profile_name=settings.MY_PROFILE_NAME,
                                                code=stone.code)
    return url
