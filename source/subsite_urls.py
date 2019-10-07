#-*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'apps.website.subsite_views.website_index', name='index'),
                       url(r'^w/', include('apps.website.subsite_urls')),
                       url(r'^p/', include('apps.pages.subsite_urls')),
                       url(r'^n/', include('apps.news.subsite_urls')),
                       url(r'^f/', include('apps.feedback.subsite_urls')),
                       )

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
