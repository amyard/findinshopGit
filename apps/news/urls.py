#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from apps.news import views

urlpatterns = patterns('',
    url(r'^all/$', views.news, name='news'),
    url(r'^add/$', views.news_add, name='news_add'),
    url(r'^(?P<news_id>\d+)/d/$', views.news_delete, name='news_delete'),
    url(r'^(?P<news_id>\d+)/e/$', views.news_edit, name='news_edit'),
)
