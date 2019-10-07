#-*- coding: utf-8 -*-

from django.conf.urls import url, patterns

from apps.version import views

urlpatterns = patterns('',
    url(r'^$', views.version, name='version'),
)
