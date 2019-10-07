# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from apps.cpa.views import *


urlpatterns = patterns('',
    url(r'^$', CostSettingView.as_view(), name='cost_setting'),
    url(r'^report-click/$', ReportClickView.as_view(), name='report_click'),
    url(r'^report-click-xml/(?P<report_key>[._\w]+)/$', ReportClickXMLView.as_view(), name='report_xml'),

    url(r'^get-category-cost/$', JsonCategoryCostView.as_view(), name='url_get_category_cost'),
    url(r'^get-category-cost/(?P<section_id>\d+)$', JsonCategoryCostView.as_view(), name='get_category_cost'),

    url(r'^get-category-by-site/(?P<site_id>\d+)/$', JsonUserCategoryBySiteView.as_view(), name='get_category_by_site'),
    url(r'^update-cost/$', EditCostView.as_view(), name='update_cost'),


    url(r'^transition/(?P<product_id>\d+)/$', TransitionView.as_view(), name='transition'),
)
