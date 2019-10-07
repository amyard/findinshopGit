# -*- coding: utf-8 -*-

#Python imports
import os
import time
from hashlib import md5

#Django imports
from django.db.models import Q
from django.shortcuts import _get_queryset


def create_parameter_filter(parameters):
    query = []
    for parameter in parameters:
        query.append(Q(**{'featureparameterproductconnection__parameter': parameter}))

    return query


def create_parameters_list(kwargs):
    parameters = []
    if 'filters' in kwargs:
        parameters = [int(parameter) for parameter in kwargs['filters'].split('-')]

    return parameters


def create_parameter_string(parameters_list):
    return '-'.join([str(p) for p in parameters_list])


def get_cache_parent_key(parent_id):
    return 'cache_childred_for_%s' % parent_id


def get_upload_path(section):
    def get_section_path(instance, filename):
        ext = filename.rsplit('.', 1)[-1]
        # if ext not in ('jpg', 'png', 'gif', 'jpeg', 'xls'):
        #     ext = 'jpg'
        hash = md5(str(time.time())).hexdigest()
        return os.path.join('', section, '%s.%s' % (hash, ext))
    return get_section_path


def get_section_path(instance, filename):
    ext = filename.rsplit('.', 1)[-1]
    # if ext not in ('jpg', 'png', 'gif', 'jpeg', 'xls'):
    #     ext = 'jpg'
    hash = md5(str(time.time())).hexdigest()
    return os.path.join('', instance.get_section(), '%s.%s' % (hash, ext))


def get_obj_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except:
        return None


class EnumChoices(object):
    """
    This is class to help using choices for fields in code. e.g.:
      Defined model:
        class Company(models.Model):
            STATUS = EnumChoices((
                (0, _('Closed'), 'CLOSED'),
                (1, _('Active'), 'ACTIVE'),
            ))
            status = models.IntegerField(_('Status'), choices=STATUS)
      Using in code:
        >>> import Company
        >>> c = Company(status=Company.STATUS.ACTIVE)
        >>> c.status == Company.STATUS.ACTIVE
        True
        >>> c.status == Company.STATUS.CLOSED
        False
    """

    def __init__(self, choices):
        self._enums = {}
        self._choices = []
        self._enums_reverse = {}
        for choice in choices:
            self._enums[choice[2]] = choice[0]
            self._enums_reverse[choice[0]] = choice[2]
            self._choices.append((choice[0], choice[1]))

    def __iter__(self):
        return iter(self._choices)

    def __getattr__(self, name):
        try:
            return self._enums[name]
        except KeyError:
            raise AttributeError("%r object has no attribute %r" %
                                 (type(self).__name__, name))

    def __contains__(self, item):
        return item in self._enums.values()

    def get_name(self, key):
        return self._enums_reverse.get(key, '')

    def get_title(self, key):
        return dict(self._choices).get(key, '')

    def add_choice(self, choice):
        self._enums[choice[2]] = choice[0]
        self._enums_reverse[choice[0]] = choice[2]
        self._choices.append((choice[0], choice[1]))
