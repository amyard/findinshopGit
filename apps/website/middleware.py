# coding: utf-8

import time

from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils.http import cookie_date
from importlib import import_module
from django.http import HttpResponseRedirect
from models import Website


class MultiDomainMiddleware(object):

    def process_request(self, request):
        host = request.META.get('HTTP_HOST')
        path_info = request.META.get('PATH_INFO') if not request.META.get('PATH_INFO') == '/' else ''
        query_string = request.META.get('QUERY_STRING', '')
        if query_string:
            uri = '%s?%s' % (path_info, query_string.decode('utf-8'))
        else:
            uri = '%s' % path_info

        if host:
            if settings.BASE_DOMAIN in host:
                subdomain = host.replace(settings.BASE_DOMAIN, '')
                if subdomain:

                    if subdomain == 'www' or subdomain == 'www.':
                        #g = GeoIP(settings.GEOIP_FILE_PATH)
                        country = g.country(request.META.get('REMOTE_ADDR'))
                        #if country['country_code'] == 'RU':
                        #    return HttpResponseRedirect('http://findinshop.ru%s' % uri)
                        #else:
                        return HttpResponseRedirect('http://%s%s' % (settings.BASE_DOMAIN, uri))

                    if subdomain[-1] == '.':
                        subdomain = subdomain[:-1]
                    else:
                        return HttpResponseRedirect('http://%s%s' % (settings.BASE_DOMAIN, uri))
                #else:
                #    g = GeoIP(settings.GEOIP_FILE_PATH)
                #    country = g.country(request.META.get('REMOTE_ADDR'))
                #    if country['country_code'] == 'RU':
                #        return HttpResponseRedirect('http://findinshop.ru%s' % uri)
                try:
                    if not subdomain or subdomain == 'www':
                        setattr(request, 'website', None)
                    else:
                        if Website.objects.get(subdomain=subdomain).location_site == 0:
                            setattr(request, 'website', Website.objects.get(subdomain=subdomain))
                            setattr(request, 'urlconf', 'source.subsite_urls')
                except:
                    return HttpResponseRedirect('http://%s%s' % (settings.BASE_DOMAIN, uri))
            else:
                try:
                    domain = host.replace('www.', '')
                    setattr(request, 'website', Website.objects.get(domain=domain))
                    setattr(request, 'urlconf', 'source.subsite_urls')
                except:
                    return HttpResponseRedirect('http://%s%s' % (settings.BASE_DOMAIN, uri))


class WebsiteSessionMiddleware(object):

    def process_request(self, request):
        engine = import_module(settings.SESSION_ENGINE)
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
        request.session = engine.SessionStore(session_key)

    def process_response(self, request, response):
        try:
            accessed = request.session.accessed
            modified = request.session.modified
        except AttributeError:
            pass
        else:
            if accessed:
                patch_vary_headers(response, ('Cookie',))
            if modified or settings.SESSION_SAVE_EVERY_REQUEST:
                if request.session.get_expire_at_browser_close():
                    max_age = None
                    expires = None
                else:
                    max_age = request.session.get_expiry_age()
                    expires_time = time.time() + max_age
                    expires = cookie_date(expires_time)
                if response.status_code != 500:
                    request.session.save()
                    response.set_cookie(settings.SESSION_COOKIE_NAME,
                                        request.session.session_key, max_age=max_age,
                                        expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                                        path=settings.SESSION_COOKIE_PATH,
                                        secure=settings.SESSION_COOKIE_SECURE or None,
                                        httponly=settings.SESSION_COOKIE_HTTPONLY or None)
                    if request.user.is_authenticated():
                        response.set_cookie(settings.SESSION_COOKIE_NAME,
                                            request.session.session_key, max_age=max_age,
                                            expires=expires, domain='%s' % request.user.website.domain,
                                            path=settings.SESSION_COOKIE_PATH,
                                            secure=settings.SESSION_COOKIE_SECURE or None,
                                            httponly=settings.SESSION_COOKIE_HTTPONLY or None)
        return response


class WebsitePrivateSessionMiddleware(object):

    def process_request(self, request):
        engine = import_module(settings.SESSION_ENGINE)
        session_key = request.COOKIES.get('wpm_' + settings.SESSION_COOKIE_NAME, None)
        request.website_private_session = engine.SessionStore(session_key)

    def process_response(self, request, response):
        try:
            accessed = request.website_private_session.accessed
            modified = request.website_private_session.modified
        except AttributeError:
            pass
        else:
            if accessed:
                patch_vary_headers(response, ('Cookie',))
            if modified or settings.SESSION_SAVE_EVERY_REQUEST:
                if request.website_private_session.get_expire_at_browser_close():
                    max_age = None
                    expires = None
                else:
                    max_age = request.website_private_session.get_expiry_age()
                    expires_time = time.time() + max_age
                    expires = cookie_date(expires_time)
                if response.status_code != 500:
                    request.website_private_session.save()
                    host = request.META.get('HTTP_HOST')
                    if settings.BASE_DOMAIN in host:
                        domain = '%s.%s' % (request.website.subdomain, settings.BASE_DOMAIN)
                    else:
                        domain = host
                    response.set_cookie('wpm_' + settings.SESSION_COOKIE_NAME,
                                        request.website_private_session.session_key, max_age=max_age,
                                        expires=expires, domain=domain,
                                        path=settings.SESSION_COOKIE_PATH,
                                        secure=settings.SESSION_COOKIE_SECURE or None,
                                        httponly=settings.SESSION_COOKIE_HTTPONLY or None)

        return response
