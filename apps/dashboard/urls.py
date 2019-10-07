from django.conf.urls import patterns, url, include

from apps.dashboard import views

urlpatterns = patterns('',
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^logout/$',views.logout),
    # url(r'^login_user/$',views.login_user, name = 'login_user'),
    url(r'^register_user/$',views.register_user, name='register_user'),
    url(r'^login_user/$', views.LoginFormView.as_view(),name='login_user'),
    url(r'^test/$', views.test),
    url(r'^(history)/$', views.HistoryView.as_view(), name='history'),
    url(r'^(wishlist)/$', views.HistoryView.as_view(), name='wishlist'),
    url(r'^ip/$',views.geolocation),
    
                        )
