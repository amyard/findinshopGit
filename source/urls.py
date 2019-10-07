#-*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from apps.website.views import SearchView
from apps.account.views import (
    SignupOnlineMarketFormView,
    SignupOfflineMarketFormView
)

CACHE_TIMEOUT_SEARCH = 20*60 #20 minutes

admin.autodiscover()

urlpatterns = patterns('',
  
                       url(r'^admin/mailto/$', 'apps.dashboard.admin.mailto', name='mailto'),
                       url(r'^$', 'apps.website.views.index', name='index'),

                       #url(r'^search/$', 'apps.website.views.search',  name='search'),
                       #url(r'^search/$', cache_page(CACHE_TIMEOUT_SEARCH)(SearchView.as_view()), name='search'),
                       url(r'^search/$', SearchView.as_view(),  name='search'),
                       url(r'^asearch/$', 'apps.website.views.search_autocomplete', name='search_autocomplete'),

                       url(r'^website/$', 'apps.website.views.website', name='website'),

#                       url(r'^about/$', TemplateView.as_view(template_name="about.html"), name='about'),
#                       url(r'^dealers/$', TemplateView.as_view(template_name="dealers.html"), name='dealers'),
#                       url(r'^jobs/$', TemplateView.as_view(template_name="jobs.html"), name='jobs'),
#                       url(r'^price/$', TemplateView.as_view(template_name="price.html"), name='price'),

                       url(r'^connect_shop/$', 'apps.feedback.views.connect_shop', name='connect_shop'),
                       url(r'^connect_shop/send/$', 'apps.feedback.views.connect_shop_send', name='connect_shop_send'),

#                       url(r'^advertisement/$', TemplateView.as_view(template_name="advertisement.html"), name='advertisement'),
#                       url(r'^protect/$', TemplateView.as_view(template_name="protect.html"), name='protect'),

                       url(r'^support/$', 'apps.feedback.views.support', name='support'),

                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name='logout'),
                       # TODO remove
                       url(r'^signup/$', 'apps.account.views.signup', name='signup'),
                       url(r'^signup2/$', 'apps.account.views.signup2', name='signup2'),
                       url(r'^signup3/$', 'apps.account.views.signup3', name='signup3'),

                       url(r'^signup_online/$', SignupOnlineMarketFormView.as_view(), name='signup_online'),
                       url(r'^signup_offline/$', SignupOfflineMarketFormView.as_view(), name='signup_offline'),

                       url(r'^admin/', include(admin.site.urls)),
                    #    url(r'^force_reindex/$', 'apps.website.views.force_update_index', name='force_index_update'),

                       url(r'^banner/', include('apps.banner.urls')),
                       url(r'^dashboard/', include('apps.dashboard.urls')),

                       url(r'^a/', include('apps.account.urls')),
                       url(r'^w/', include('apps.website.urls')),
                       url(r'^c/', include('apps.catalog.urls')),
                       url(r'^p/', include('apps.pages.urls')),
                       url(r'^n/', include('apps.news.urls')),
                       url(r'^v/', include('apps.version.urls')),
                       url(r'^t/', include('apps.ticket.urls')),
                       url(r'^d/', include('apps.distribution.urls')),
                       
                       #url(r'^api/v1/', include('apps.api_rest.urls')),

                       url(r'^section/', include('apps.section.urls')),
                       url(r'^bid/', include('apps.cpa.urls')),
                       url(r'^coupon/', include('apps.coupon.urls')),
                       url(r'^page/', include('django.contrib.flatpages.urls')),
                )

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
