#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from apps.website import views
from apps.website.views import CouponSettingsView

urlpatterns = patterns('',
                       url(r'^s/$', views.site_settings, name='site_settings'),
                       url(r'^t/$', views.spaces, name='spaces'),
                       url(r'^validate_coupon_form/$', views.validate_coupon_form, name='validate_coupon_form'),
                       url(r'^coupon_settings/$', CouponSettingsView.as_view(), name='coupon_settings'),

                       # url(r'^validate_coupon_form/', views.ValidateCouponForm.as_view(), name='validate_coupon_form'),

                       url(r'^t/e/(?P<space_id>\d+)/$', views.spaces_edit, name='spaces_edit'),
                       url(r'^cookie.js$', views.create_cookie_js, name='create_cookie'),
                       url(r'^gti/$', views.get_item_info, name='get_item_info'),
                       url(r'^filter-setting/$', views.filter_setting, name='filter_setting'),
                       # url(r'^sphinx_test/$', views.sphinx_test),
                       url(r'^wishlist/', views.wishlist),
                       
                       )
