#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from apps.banner import views

urlpatterns = patterns('',
                       url(r'^get/(?P<user_id>\d+)/$', views.get, name='get'),
                       )
