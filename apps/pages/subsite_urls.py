#-*- coding: utf-8 -*-

from django.conf.urls import url, patterns

from apps.pages import subsite_views as views

urlpatterns = patterns('',
       url(r'^(?P<page_id>\d+)/$', views.page, name='page'),
)
