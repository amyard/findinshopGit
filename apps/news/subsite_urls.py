#-*- coding: utf-8 -*-

from django.conf.urls import url, patterns

from apps.news import subsite_views as views

urlpatterns = patterns('',
       url(r'^(?P<news_id>\d+)/$', views.news, name='news'),
       url(r'^all/$', views.news_all, name='news_all'),
)
