# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _


READER_ERRORS_MAP = {
    'R001': _(u'ImportTask not found'),
    'R002': _(u'ImportTask url not found'),
    'R003': _(u'Url not response'),
    'R999': _(u'Unknown error'),
}


class ReaderException(Exception):
    def __init__(self, message=None, code='R999'):
        self.code = code
        self.message = message or self.get_message()
        super(ReaderException, self).__init__(self.message)

    def get_message(self):
        return READER_ERRORS_MAP[self.code]
