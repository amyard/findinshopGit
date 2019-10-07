from django.core.cache import cache
from django.conf import settings


class PresenceMiddleware(object):

    def process_request(self, request):
        if request.user.is_authenticated():
            cache.set(settings.PRESENCE_KEY % request.user.id, True, settings.PRESENCE_TIMEOUT)

