# coding: utf-8

from django.utils import timezone
from django.views.generic import View
from django.http import HttpResponse

from .models import Mingpian, Philosopherstone


class ProfileView(View):
    def get(self, request, code):
        # check code validity
        try:
            stone = Philosopherstone.objects.get(code=code)
            create_datetime = stone.create_datetime
            current_datetime = timezone.now()
            timedelta_seconds = (current_datetime-create_datetime).seconds
            if timedelta_seconds > 120:
                return HttpResponse('time out')
                # pass #超时
            else:
                return HttpResponse('ok')
                # pass # 返回表单
        except Philosopherstone.DoesNotExist:
            # pass
            # 无效
            return HttpResponse('invalid code')
