#-*- coding: utf-8 -*-

from django.contrib.sites.models import Site
from django.conf import settings as _settings


def site(request):
    return {'site': Site.objects.get_current()}


def settings(request):
    return {'settings': _settings}
