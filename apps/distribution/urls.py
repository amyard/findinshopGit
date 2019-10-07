from django.conf.urls import patterns, url

urlpatterns = patterns('apps.distribution.views',
                       url(r'^add/$', 'add_subscriber', name='add_subscriber'),
                       url(r'^deactivate/$', 'deactivate', name='deactivate'),
                       )
