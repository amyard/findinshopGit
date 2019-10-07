# -*- coding: utf-8 -*-

#Django imports
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class AdminMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser == 0:
            raise Http404

        return super(AdminMixin, self).dispatch(request, *args, **kwargs)
