# -*- coding: utf-8 -*-

from django.core.mail import send_mail
from django.template.loader import render_to_string

from apps.catalog.models import Item, Category


def send_coupon_message(coupon):
    obj = ''
    if 'category' in coupon.filters:
        category = Category.objects.get(id=coupon.filters.split('=')[1])
        obj = 'category'
    elif coupon.filters.startswith('id'):
        product = Item.objects.get(id=coupon.filters.split('=')[1])
        obj = 'product'

    message = u'Купон для %s, Размер скидки: %s, Действие от %s до %s.' % (
                    category.name if obj == 'category' else product.name,
                    coupon.size,
                    coupon.date_start,
                    coupon.date_end
            )

    send_mail(u'Создание купона на FINDINSHOP', message, 'no-reply@findinshop.com',
        [coupon.user.email], fail_silently=False)


def send_coupon_user(user_email, name='coupon', context={}):
    message = render_to_string('mail/{}.html'.format(name), context)
    subject = u'Ваш купон - FINDINSHOP.COM'
    send_mail(
        subject, message, 'no-reply@findinshop.com',
        (user_email,), fail_silently=False)

def send_coupon_store(coupon, user_name):
    send_mail(u'Купон от FINDINSHOP', u'Купоном для %s воспользовался %s' % (coupon, user_name), 'no-reply@findinshop.com',
    [coupon.user.email], fail_silently=False)


def send_coupon_report(coupon):
    print coupon.count
    send_mail(u'Купон от FINDINSHOP', u'У вашего купона истек срок активности. Всего воспользовалось купоном пользователей: %s' % (coupon.count), 'no-reply@findinshop.com',
    [coupon.user.email], fail_silently=False)
