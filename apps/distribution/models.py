# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _

from utils.enum_choices import EnumChoices
from apps.catalog.models import Item
from apps.coupon.models import Coupon


class Subscriber(models.Model):
    STATUSES = EnumChoices((
        (0, u'Не подписан', 'UNSUBSCRIBED'),
        (1, u'Подписан', 'SUBSCRIBED'),
    ))

    class Meta:
        verbose_name = u'Подписчик'
        verbose_name_plural = u'Подписчики'
        ordering = ["-status", "email"]

    first_name = models.CharField(verbose_name=u'Имя', max_length=64, blank=True, null=True)
    last_name = models.CharField(verbose_name=u'Фамилия', max_length=64, blank=True, null=True)
    phone = models.CharField(verbose_name=u'Телефон', max_length=50, null=True, blank=True)
    email = models.EmailField(verbose_name=u'Email', unique=False, null=True, blank=True)
    status = models.IntegerField(verbose_name=u'Статус', choices=STATUSES, default=1)

    def __unicode__(self):
        return self.email


class CouponSubscriber(models.Model):
    subscriber = models.ForeignKey(Subscriber)
    coupon = models.ForeignKey(Coupon)
    product_name = models.CharField(
        verbose_name=u'Наименование', max_length=4000,
        default=u'Нет названия продукта')
    product_group = models.CharField(
        u'Группа товаров', max_length=150, null=True)
    market_name = models.CharField(
        max_length=255,
        verbose_name=u'Название магазина который предоставил купон',
        null=True)
    price = models.FloatField(verbose_name=u'Цена', blank=True, null=True)
    count = models.PositiveSmallIntegerField(
        u'Количество использований', default=1)

    class Meta:
        verbose_name = _(u'Заказные купоны')
        verbose_name_plural = _(u'Заказные купоны')

    def __unicode__(self):
        return u'%s-%s' % (self.subscriber.first_name, self.coupon.code)

    def get_user_information(self):
        return '<a href="/admin/distribution/subscriber/%s">%s; %s; %s</a>' % (
            self.subscriber.id,
            self.subscriber.first_name if self.subscriber.first_name else '',
            self.subscriber.email if self.subscriber.email else '',
            self.subscriber.phone if self.subscriber.phone else ''
        )
    get_user_information.short_description = _(
        u'Имя; Электронный адрес; Телефон')
    get_user_information.allow_tags = True


class Letter(models.Model):
    STATUSES = EnumChoices((
        (0, u'В ожидании', 'PENDING'),
        (1, u'Завершена', 'DONE'),
    ))

    class Meta:
        verbose_name = u'Письмо'
        verbose_name_plural = u'Письма'
        ordering = ["-status", "date"]

    title = models.CharField(verbose_name=u'Тема', max_length=100, unique=True)
    text = models.TextField(verbose_name=u'Содержание', blank=True, null=True)
    date = models.DateField(verbose_name=u'Дата для рассылки')
    recipients = models.ManyToManyField(Subscriber, verbose_name=u'Получатели')
    status = models.IntegerField(verbose_name=u'Статус', choices=STATUSES, default=0)

    def __unicode__(self):
        return self.title
