#-*- coding: utf-8 -*-

from django.conf.urls import url, patterns

from apps.feedback import subsite_views as views

urlpatterns = patterns('',
    url(r'^$', views.feedback, name='feedback'),
    url(r'^sent/(?P<status>\d)/$', views.feedback_sent, name='feedback_sent'),
)
