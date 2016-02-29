# encoding: utf-8

from django.conf.urls import url

from .views import ReceiveView

urlpatterns = [
    url(r'^weixin$', ReceiveView.as_view(), name='receive'),
]
