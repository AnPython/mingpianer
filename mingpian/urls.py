# coding: utf-8

from django.conf.urls import url

from .views import ProfileView, DashboardView, transfer_valid, MultiSearchView

urlpatterns = [
    url(r'^profile/(?P<code>[a-z0-9]+?)$', ProfileView.as_view(), name='profile'),
    url(r'^search/(?P<code>[a-z0-9]+?)$', MultiSearchView.as_view(), name='search'),
    url(r'^dashboard$', DashboardView.as_view(), name='dashboard'),
    url(r'^valid$', transfer_valid, name='valid'),
]
