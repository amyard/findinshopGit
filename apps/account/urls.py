#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from apps.account import views
# from apps.account.oauth2 import vkontakte


    # (r'^about/', TemplateView.as_view(template_name="about.html")),

urlpatterns = patterns('',
       url(r'^(?P<uid>\d+)/$', views.account_page, name='account_page'),
       url(r'^(?P<uid>\d+)o/$', views.account_other, name='account_other'),
       url(r'^$', views.account, name='account'),
       url(r'^s/$', views.settings, name='account_settings'),
       url(r'^ss/$', views.social, name='account_social'),

       url(r'^sct/$',TemplateView.as_view(template_name="themes/findinshop/red/signup_complete.html"), name='signup_complete'),
       url(r'^sctint/$',TemplateView.as_view(template_name="themes/findinshop/red/signup_complete2.html"), name='signup_complete2'),
       url(r'^scf/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', views.activate, name='signup_confirmation'),
       url(r'^sd/$', TemplateView.as_view(template_name="signup_done.html"), name='signup_done'),
       url(r'^sac/$',TemplateView.as_view(template_name="signup_already_active.html"), name='signup_already_active'),
       url(r'^sil/$', TemplateView.as_view(template_name="signup_invalid_link.html"), name='signup_invalid_link'),
       url(r'^pr/$', 'django.contrib.auth.views.password_reset', {'template_name': 'password_reset.html'}, name='password_reset'),
       url(r'^prcf/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'password_reset_confirm.html'}, name='auth_password_reset_confirm'),
       url(r'^prcp/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'password_reset_complete.html'}, name='auth_password_reset_complete'),
       url(r'^prd/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'password_reset_done.html'}, name='auth_password_reset_done'),
       url(r'^pc/$', 'django.contrib.auth.views.password_change', {'template_name': 'password_change.html'}, name='password_change'),
       url(r'^pcd/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'password_change_done.html'}, name='password_change_done'),

       url(r'^pcuo/$', 'django.contrib.auth.views.password_change', {'template_name': 'password_change_us_online.html'}, name='password_change_us_online'),
       url(r'^pcuo/$', 'django.contrib.auth.views.password_change_done', {'template_name': ''}, name='password_change_done_us_online'),
       # OAuth2 section
       # url(r'^o2/vkcb/$', vkontakte.callback, name='oauth2_vk_callback'),
       )
