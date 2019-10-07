#-*- coding: utf-8 -*-

import json
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.http import HttpResponseForbidden

from apps.website.models import Website
from apps.version.models import Version


def render_to(template_path, allow_ajax=False):
    """
    Decorate the django view.

    Wrap view that return dict of variables, that should be used for
    rendering the template.
    Dict returned from view could contain special keys:
    * MIME_TYPE: mimetype of response
    * TEMPLATE: template that should be used instead one that was
                specified in decorator argument
    """

    def decorator(func):
        def wrapper(request, *args, **kwargs):
            output = func(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            kwargs = {'context_instance': RequestContext(request)}

            if allow_ajax and request.is_ajax():
                return HttpResponse(json.dumps(output), 'application/json')

            if 'MIME_TYPE' in output:
                kwargs['mimetype'] = output.pop('MIME_TYPE')
            template = template_path
            if 'TEMPLATE' in output:
                template = output.pop('TEMPLATE')
            return render_to_response(template, output, **kwargs)
        return wrapper
    return decorator


def r_to(template_name):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            out = func(request, *args, **kwargs)
            if not isinstance(out, dict):
                return out
            return render(request, 'themes/' + Website.SKINS._enums_reverse[int(request.website.skin)].lower() + '/' + template_name, out)
        return wrapper
    return decorator


def check_subsite_version(version):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            out = func(request, *args, **kwargs)
            if getattr(request.website.user.versions, Version.TYPE.get_name(version)):
                return out
            else:
                return HttpResponseForbidden()
        return wrapper
    return decorator
