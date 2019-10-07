# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

#Apps imports
from apps.catalog.models import Item, Category


DISCOUNT_TYPE_CHOICES = (
    ('P', 'Процентная'),
    ('F', 'Фиксированная'),
)


class Coupon(models.Model):
    user = models.ForeignKey(User)
    code = models.CharField(u'Код купона', max_length=255, help_text=u'! Можете указать свой код')
    size = models.PositiveSmallIntegerField(u'Размер скидки')
    types = models.CharField('Тип скидки', max_length=1, choices=DISCOUNT_TYPE_CHOICES, default=DISCOUNT_TYPE_CHOICES[0][0])
    date_start = models.DateTimeField(u'Купон действует с', help_text=u'Формат: число.месяц.год часы:минуты:секунды. По умолчанию с момента создания')
    date_end = models.DateTimeField(u'Купон действителен до', help_text=u'Формат: число.месяц.год часы:минуты:секунды.')
    items = models.ManyToManyField(Item, verbose_name=u'Товары')
    count = models.PositiveSmallIntegerField(u'Количество использований', default=0)
    filters = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.BooleanField('Удален?', default=False)

    def __unicode__(self):
        return u'%s' % self.code

    def name_category(self):
        """
        Get catalog name
        :return:
        """
        # TODO put this in database field
        if 'category' in self.filters:
            try:
                category_id = self.filters.split('=')[1]
                return Category.objects.get(pk=category_id).name
            except Exception:
                return "Unknown"
        elif self.filters.startswith('id'):
            try:
                return Item.objects.get(id=self.filters.split('=')[1]).name
            except Item.DoesNotExist:
                return "Unknown"

    class Meta:
        verbose_name = u'Купон'
        verbose_name_plural = u'Купоны'
        unique_together = ('user', 'code')
