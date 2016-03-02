# coding: utf-8

from django.conf.urls import url
from django.conf import settings

from .views import ProfileView, DashboardView, transfer_valid

urlpatterns = [
    url(r'^%s/(?P<code>[a-z0-9]+?)$' % settings.MY_PROFILE_NAME, ProfileView.as_view(), name='profile'),
    url(r'^dashboard$', DashboardView.as_view(), name='dashboard'),
    url(r'^valid$', transfer_valid, name='valid'),
]
