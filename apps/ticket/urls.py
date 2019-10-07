#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from apps.ticket import views

urlpatterns = patterns('',
                       url(r'^all/$', views.tickets, name='tickets'),
                       url(r'^new/$', views.ticket_add, name='ticket_add'),
                       url(r'^(?P<ticket_id>\d+)/(?P<action>\w+)/$', views.ticket_control, name='ticket_control'),
                       )
