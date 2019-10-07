# -*- coding: utf-8 -*-

def float_to_python(value):
    try:
        return float(str(value).replace(',', '.'))
    except:
        return 0


def get_item_unique_cookie_key(item):
    return 'uniq_item_%s' % item.pk


def get_report_cookie_key(user, date_from, date_to):
    return 'report_%s_%s_%s' % (user.id,
                                get_str_date(date_from),
                                get_str_date(date_to)
                )


def get_str_date(date):
    return date.strftime("%d.%m.%Y")
