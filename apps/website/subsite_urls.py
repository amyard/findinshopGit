from django.conf.urls import patterns, url

from apps.website import subsite_views as views, bank_views

urlpatterns = patterns('',
                       url(r'^$', views.website_index, name='index'),
                       url(r'^f/(?P<cat_id>\d+)/$', views.filter_by_cat, name='filter_by_cat'),
                       url(r'^ip/(?P<item_id>\d+)/$', views.item_page, name='item_page'),

                       url(r'^a2b/(?P<item_id>\d+)/$', views.add_to_basket, name='add_to_basket'),
                       url(r'^cb/$', views.clean_basket, name='clean_basket'),
                       url(r'^rfb/(?P<pos>\d+)/$', views.rm_from_basket, name='remove_from_basket'),
                       url(r'^vb/$', views.view_basket, name='view_basket'),
                       url(r'^rc/$', views.recalculate, name='recalculate'),

                       url(r'^order/$', views.order, name='order'),
                       url(r'^order/send/$', views.make_order, name='make_order'),
                       url(r'^order/(?P<status>\d+)/$', views.order, name='order_status'),

                       url(r'^order/(?P<status>\d+)/(?P<order_id>\d+)/$', views.order, name='order_status'),
                       url(r'^order/(?P<status>\d+)/(?P<order_id>\d+)/(?P<stat_b>\d+)$', views.order, name='order_status'),

                       url(r'^search/$', views.search, name='search'),

                       url(r'^export/$', views.exportYML, name='exportYML'),

                       url(r'^bank/$', bank_views.data_bank, name='data_bank'),


                       )
