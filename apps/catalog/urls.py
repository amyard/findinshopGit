#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from apps.catalog import views

urlpatterns = patterns('',
                       url(r'^s/$', views.catalog, name='catalog'),

                       url(r'^(?P<cat_id>\d+)/ia/$', views.add_item, name='add_item'),
                       url(r'^ei/(?P<item_id>\d+)/$', views.edit_item, name='edit_item'),
                       url(r'^di/(?P<item_id>\d+)/$', views.delete_item, name='delete_item'),
                       # url(r'^(?P<cat_id>\d+)/(?P<item_id>\d+)/$', views.item, name='item'),
                       # url(r'^(?P<cat_id>\d+)/(?P<item_id>\d+)/e/$', views.item, name='item_edit'),
                       # url(r'^(?P<cat_id>\d+)/(?P<item_id>\d+)/d/$', views.item, name='item_delete'),
                       url(r'^set/top/$', views.bestseller, name='set_bestseller'),

                       url(r'^(?P<cat_id>\d+)/$', views.category, name='category'),
                       url(r'^ac/$', views.category_add, name='category_add'),
                       url(r'^(?P<cat_id>\d+)/e/$', views.category_edit, name='category_edit'),
                       url(r'^(?P<cat_id>\d+)/d/$', views.category_delete, name='category_delete'),

                       url(r'^ex/(?P<action>\w+)/$', views.export_task, name='export_task'),
                       url(r'^ex/(?P<action>\w+)/(?P<task_id>\d+)/$', views.export_task, name='del_export_task'),

                       url(r'^orders/$', views.orders, name='orders'),
                       url(r'^orders/(?P<order_id>\d+)/(?P<action>\w+)/$', views.order_control, name='order_control'),

                       url(r'^im/t/$', views.import_task, name='import_task'),
                       url(r'^im/t2/$', views.import_task_YML, name='import_task_YML'),
                       url(r'^im/t3/$', views.import_task_Excel, name='import_task_Excel'),
                       url(r'^im/t4/$', views.import_task_HotPrise, name='import_task_HotPrise'),
                       url(r'^im/t5/$', views.import_task_1c, name='import_task_1c'),
                       url(r'^im/h/$', views.import_status, name='import_status'),
                       url(r'^im/e/$', views.import_error, name='import_error'),
                       url(r'^im/r/(?P<task_id>\d+)/$', views.import_restart, name='import_restart'),
                       url(r'^im/s/(?P<task_id>\d+)/$', views.import_stop, name='import_stop'),
                       url(r'^im/d/(?P<task_id>\d+)/$', views.import_disable, name='import_disable'),



                       url(r'^1c/(?P<user_id>\d+)/$', views.import_1c, name='import_1c'),

                       url(r'^flush/(?P<status_code>\w+)/$', views.flush_catalog, name='flush_catalog'),

                       url(r'^o/f/$', views.filter, name='filter'),
                       url(r'^o/inform/$', views.information, name='information'),
                       url(r'^point/add/$', views.point_add, name='point_add'),
                       url(r'^points/$', views.points, name='points'),
                       url(r'^point/edit/(?P<point_id>\d+)/$', views.point_add, name='point_edit'),
                       url(r'^point/delete/(?P<point_id>\d+)/$', views.point_delete, name='point_delete'),
                       url(r'^map/stores/(?P<user_id>\d+)/$', views.map_stores, name='map_stores'),


                       # url(r'^o/payments/$', views.payments, name='payments'),
                       )
