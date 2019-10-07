#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from apps.pages import views

urlpatterns = patterns('',
                       url(r'^all/$', views.pages, name='pages'),
                       url(r'^add/$', views.pages_add, name='pages_add'),
                       url(r'^(?P<page_id>\d+)/d/$', views.pages_delete, name='pages_delete'),
                       url(r'^(?P<page_id>\d+)/e/$', views.pages_edit, name='pages_edit'),
                       )
