#-*- coding:utf-8 -*-

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
