# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
# from django.contrib.contenttypes import generic

from utils.enum_choices import EnumChoices
from utils.transliterate import transliterate


class Page(models.Model):
    TYPES = EnumChoices((
        (0, u'Встроенная страница', 'BUILT-IN'),
        (1, u'Пользовательская страница', 'CUSTOM'),
    ))
    POSITION = EnumChoices((
        (0, u'Отсутствует', 'NONE'),
        (1, u'Шапка страницы', 'HEADER'),
        (2, u'Основание страницы', 'FOOTER'),
    ))
    website = models.ForeignKey('website.Website', blank=True, null=True, related_name='pages')
    title = models.CharField(verbose_name=u'Название', max_length=255)
    text = models.TextField(verbose_name=u'Содержание')
    slug = models.SlugField()
    visibility = models.BooleanField('Опубликована', default=True, help_text="Поставьте эту отметку если страница уже закончена и готова к публикации")
    date = models.DateTimeField(verbose_name=u'Дата', auto_now_add=True)
    page_type = models.IntegerField(choices=TYPES, default=1)
    position = models.IntegerField(verbose_name=u'Расположение', choices=POSITION, default=1)

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self.__class__)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('page', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(transliterate(self.title))
        super(Page, self).save(*args, **kwargs)

    def get_position(self):
        if self.position:
            return '%s' % Page.POSITION.get_name(self.position)
        else:
            return None

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
        unique_together = ('website', 'slug')
        ordering = ['page_type', '-title']
