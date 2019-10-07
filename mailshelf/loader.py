#-*- coding: utf-8 -*-

from django.core.cache import cache

from models import Message

EMAIL_CACHE_KEY = 'email_'

class MessageLoader(object):

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MessageLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __getattr__(self, key):
        # check self first
        try:
            value = super(MessageLoader, self).__getattr__(key)
            return value
        except AttributeError:
            pass

        # check cache
        cache_key = '%s%s' % (EMAIL_CACHE_KEY, key)
        value = cache.get(cache_key)
        if value:
            setattr(self, key, value)
            return value

        # try to pull from db
        try:
            value = Message.objects.get(key=key)
            setattr(self, key, value)
            cache.set(cache_key, value)
            return value
        except Message.DoesNotExist:
            return None


