# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from apps.coupon.views import *


urlpatterns = patterns('',
    url(r'^create/$', CouponCreateView.as_view(), name='coupon_create'),
    url(r'^list/$', CouponsView.as_view(), name='coupons'),
    url(r'^delete/(?P<pk>\d+)/$', CouponDeleteView.as_view(), name='coupon_delete'),
)
