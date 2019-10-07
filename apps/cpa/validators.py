# -*- coding: utf-8 -*-

#Django imports
from django.core.exceptions import ValidationError


MIN_COST_RATE = 0


def min_cost_rate(value):
    if value < MIN_COST_RATE:
        raise ValidationError(u'Минимальное стоимость не может быть меньше %s грн' % MIN_COST_RATE)

    return value
