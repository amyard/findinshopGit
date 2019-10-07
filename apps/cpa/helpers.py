# -*- coding: utf-8 -*-

#Findinshop imports
from apps.cpa.models import CostSetting


def get_caterogy_with_cost(user, sections):
    #TODO: Cache
    for section in sections:
        setting, created = CostSetting.objects.get_or_create(user=user, section=section)

        section.count_item = setting.count_item
        section.base_cost = setting.base_cost
        section.current_rate = setting.current_rate
        section.total_cost = setting.total_cost

    return sections
