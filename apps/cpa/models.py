# -*- coding: utf-8 -*-

#Django imports
from django.db import models
from django.contrib.auth.models import User

#findinshop
from apps.section.utils import EnumChoices
from apps.catalog.models import Item, Category
from apps.website.models import Website
from apps.section.models import Section
from apps.cpa.validators import min_cost_rate


BASE_COST = 0


class CostSetting(models.Model):
    user = models.ForeignKey(User)
    section = models.ForeignKey(Section)
    count_item = models.IntegerField(u'Количество товаров в разделе', default=0)
    base_cost = models.FloatField(u'Базовая стоимость клика', default=BASE_COST)
    current_rate = models.FloatField(u'Текущая ставка', default=0, validators=[min_cost_rate])
    total_cost = models.FloatField(u'Общая стоимость клика', default=0)
    date_change = models.DateTimeField(auto_now=True)
    changed = models.BooleanField(u'Менялась ставка?', default=False)

    def __unicode__(self):
        return u'Настройки стоимости клика для %s' % self.user


class Report(models.Model):
    user = models.ForeignKey(User)
    section = models.ForeignKey(Section, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True)
    product_name = models.CharField(u'Товар', max_length=255)
    cost = models.FloatField(u'Стоимость клика')
    ip = models.CharField(u'IP адрес', max_length=20, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'Отчет о кликах'
        verbose_name_plural = u'Отчеты о кликах'


class OwnAndUserCategory(models.Model):
    site = models.ForeignKey(Website, verbose_name=u'Web сайт')
    our_section = models.ForeignKey(Section, verbose_name=u'Наш раздел')
    categories = models.ManyToManyField(
        Category, verbose_name=u'Пользовательские категории')

    def __unicode__(self):
        return u'Web сайт: %s, Категория: %s' % (self.site, self.our_section)

    class Meta:
        ordering = ('site',)
        verbose_name = u'Связь собственных и юзерских категорий'
        verbose_name_plural = u'Связи собственных и юзерских категорий'


class RefreshCostTask(models.Model):
    STATUS = EnumChoices((
        (0, u'Принят', 'NEW'),
        (1, u'Обрабатывается', 'PROCESSING'),
        (2, u'Выполнен', 'DONE'),
        (3, u'Ошибка выполнения', 'ERROR'),
    ))

    setting = models.ForeignKey(CostSetting)
    item_count = models.IntegerField(
        u'Количество переоцененных товаров', default=0)
    # Info
    status = models.IntegerField(verbose_name=u'Статус задания', choices=STATUS, default=0)
    start = models.DateTimeField(verbose_name=u'Начало выполнения', blank=True, null=True)
    complete = models.DateTimeField(verbose_name=u'Конец выполнения', blank=True, null=True)
    error = models.TextField(verbose_name=u'Код ошибки', blank=True, null=True)

    def __unicode__(self):
        return u'Задача на переоценку для %s в категории - %s' % (self.setting.user, self.setting.section)

    class Meta:
        verbose_name = u'Задание переоценки раздела'
        verbose_name_plural = u'Задания переоценки раздела'
