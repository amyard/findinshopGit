from django.conf.urls import url, include
# from rest_framework import routers
from rest_framework.routers import DefaultRouter
import views

router = DefaultRouter()
# router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^cat/$', views.ListCategory.as_view()),
    url(r'^cat/(?P<pk>[0-9]+)/$', views.DetailCategory.as_view()),
    url(r'^item/(?P<pk>[0-9]+)/$', views.DetailItem.as_view()),
    url(r'^item/$', views.ListItem.as_view()),
    url(r'^sphinx/$', views.ListItemSphinx.as_view()),
]