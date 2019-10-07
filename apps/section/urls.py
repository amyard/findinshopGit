# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from apps.section.views import *

urlpatterns = patterns('',
                       # ,
                       url(r'^$', SectionView.as_view(), name='sections'),
                       # url(r'^(?P<slug>[-_\w]+)/$', SectionView.as_view(), name='section_detail'),
                       url(r'^parse-section/parse/$', parse_hotline, name='parser_section'),

                      # url(r'^product-set/(?P<slug>[-_\w]+)/$', ProductSetView.as_view(), name='product_set'),
                       # http://findinshop.com.ua/section/elektronika/telefony/mobilnye_telefony/Xiaomi_Redmi_3_Fashion_Dark_Gray_4/

                       url(r'^(?P<slug>[-_\w]+)/$', SectionView.as_view(), name='section_detail'),
                       #url(r'^category/*/(?P<slug>[-_\w]+)/$', SectionView.as_view(), name='section_detail'),

                       url(r'^(?P<parent>[-_\w]+)/(?P<slug>[-_\w]+)/$', SectionView.as_view(),
                           name='section_detail'),
                       url(r'^(?P<root>[-_\w]+)/(?P<parent>[-_\w]+)/(?P<slug>[-_\w]+)/$',
                           SectionView.as_view(), name='section_detail'),
                       url(r'^category/(?P<root>[-_\w]+)/(?P<parent>[-_\w]+)/(?P<slug>[-_\w]+)/$',
                           SectionView.as_view(), name='section_detail'),
                       url(r'^(?P<root>[-_\w]+)/(?P<parent>[-_\w]+)/(?P<parent_1>[-_\w]+)/(?P<slug>[-_\w]+)/$',
                           SectionView.as_view(), name='section_detail'),
                       url(r'^(?P<root>[-_\w]+)/(?P<parent>[-_\w]+)/(?P<parent_1>[-_\w]+)/(?P<parent_2>[-_\w]+)/(?P<slug>[-_\w]+)/$',
                           SectionView.as_view(), name='section_detail'),
                       url(r'^(?P<root>[-_\w]+)/(?P<parent>[-_\w]+)/(?P<slug>[-_\w]+)/$', ProductView.as_view(), name='products'),
                       url(r'^(?P<root>[-_\w]+)/(?P<parent>[-_\w]+)/(?P<slug>[-_\w]+)/(?P<filters>[-\d]+)/$', ProductView.as_view(),
                           name='products'),
                       # admin urls
                       url(r'^get-parameters-for-feature/(?P<feature_id>\d+)/$', AdminJsonParameterView.as_view(),
                           name='json_parameters_feature'),
                       )
