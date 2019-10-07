# -*- coding: utf-8 -*-

# Django imports
from django.db import models
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete

# Findinshop imports
from apps.section.managers import CurrentManager, ParentSectionManage, ChildrenManage
from apps.catalog.models import Item

# epic fail: из utils.upload почему-то не импортится
from apps.section.utils import get_section_path, get_cache_parent_key


CACHE_TIMEOUT_CATEGORY = 24 * 3600  # 24 часа


class Measure(models.Model):
    inner_id = models.IntegerField(u'Внутренний id')
    name = models.CharField(u'Название', max_length=255)
    sign = models.CharField(u'Знак', max_length=255)
    sign_rus = models.CharField(u'Знак на русском', max_length=255)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = u'Мера'
        verbose_name_plural = u'Меры'


class FeatureGroup(models.Model):
    inner_id = models.IntegerField(u'Внутренний id')
    name = models.CharField(u'Название', max_length=255)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = u'Группа характеристики'
        verbose_name_plural = u'Группы характеристики'

class FeatureTypeIcecat(models.Model):
    types = models.CharField(u'Тип', max_length=255)
    
    def __unicode__(self):
        return u'%s' % self.types 

class FeatureIcecat(models.Model):
    inner_id = models.IntegerField(u'Внутренний id')
    measure = models.ForeignKey(Measure, null=True, blank=True)
    # group = models.ForeignKey(FeatureGroup, null=True, blank=True)
    name = models.CharField(u'Название', max_length=255, null=True, blank=True)
    # types = models.CharField(u'Тип', max_length=255, null=True, blank=True)
    types = models.ForeignKey(FeatureTypeIcecat, null=True, blank=True)

    def __unicode__(self):
        if not self.name is None:
            return u'%s' % self.name
        return u'id:%s' % self.inner_id

    class Meta:
        verbose_name = u'Характеристика Icecat'
        verbose_name_plural = u'Характеристики Icecat'


class Parameter(models.Model):
    name = models.CharField(u'Название', max_length=255)
    sort = models.PositiveSmallIntegerField(u'Приоритет при сортировке', default=0)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = u'Параметр'
        verbose_name_plural = u'Параметры'


class Feature(models.Model):
    admin_name = models.CharField(u'Название для админа', max_length=255,
                                  help_text=u'Для различия одинаковых характеристик: Бренды для мобильных телефонов, Бренды для автомобилей')
    name = models.CharField(u'Название', max_length=255)
    sort = models.PositiveSmallIntegerField(u'Приоритет при сортировке', default=0)
    parameters = models.ManyToManyField(Parameter, related_name='features', through='FeatureParameterConnection')

    def __unicode__(self):
        return u'%s' % self.admin_name

    class Meta:
        verbose_name = u'Характеристика'
        verbose_name_plural = u'Характеристики'


class Section(models.Model):
    SECTION_STATE = ((
        (0, u'Создан'),
        (1, u'Обрабатывается'),
        (2, u'Очищен'),
    ))

    name = models.CharField(u'Название раздела', max_length=255)
    inner_id = models.CharField(u'Название', max_length=255, blank=True, null=True)
    parse_url = models.CharField(u'Урл для парсинга', max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name=u'Родительский раздел')
    icon = models.ImageField(verbose_name=u'Лого', upload_to=get_section_path, blank=True, null=True)
    thumb = models.ImageField(verbose_name=u'Миниатюра', upload_to=get_section_path, blank=True,
                              null=True)
    description = models.TextField(u'Краткое описание раздела', blank=True, null=True)
    slug = models.SlugField(u'Slug', max_length=255)
    sort = models.PositiveSmallIntegerField(u'Приоритет при сортировке', default=0)
    features = models.ManyToManyField(Feature, verbose_name=u'Характеристики для раздела',
                                      help_text=u'Только для крайних подразделов!', blank=True)
    have_child = models.BooleanField(u'Имеет подраздел', default=False)
    deleted = models.BooleanField(u'Удален?', default=False)
    state = models.CharField(u'', max_length=255, choices=SECTION_STATE, blank=True, null=True)

    objects = CurrentManager()
    parents = ParentSectionManage()
    children = ChildrenManage()

    def __unicode__(self):
        if self.parent:
            return u'%s ---> %s' % (self.parent.name, self.name)
        return u'%s' % self.name

    def get_thumb(self):
        if self.thumb:
            return u'<img src="/media/%s" />' % self.thumb
        return 'no thumb'

    get_thumb.allow_tags = True
    get_thumb.short_description = u'Миниатюра'

    def get_slug(self):
        if self.parent is not None:
            res = "{0}/{1}".format(self.parent.get_slug(), self.slug)
        else:
            res = self.slug
        return res

    def get_children_from_parent(self):
        def _get_children_from_parent(section):
            for section in Section.objects.filter(parent=section):
                if not section.have_child:
                    children.append(section)
                else:
                    _get_children_from_parent(section)

        cache_parent_key = get_cache_parent_key(self.id)
        children = cache.get(cache_parent_key, [])

        if not children:
            for section in Section.objects.filter(parent=self):
                if section.have_child:
                    _get_children_from_parent(section)
                else:
                    children.append(section)
            cache.set(cache_parent_key, children, CACHE_TIMEOUT_CATEGORY)

        return children

    def get_all_items(self):
        children_section = [self]
        children_section.extend(self.get_children_from_parent())

        items = ProductModel.objects.filter(section__in=children_section).distinct()
        return items

    def get_section(self):
        return ('section_icon')

    class Meta:
        verbose_name = u'Раздел товаров'
        verbose_name_plural = u'Разделы товаров'


class FeatureParameterConnection(models.Model):
    feature = models.ForeignKey(Feature, related_name='parameter_connections')
    parameter = models.ForeignKey(Parameter, verbose_name=u'Параметры относящиеся к данной характеристике')

    class Meta:
        verbose_name = u'Параметры для характеристики'
        verbose_name_plural = u'Параметры для характеристики'


class ProductModel(models.Model):
    section = models.ForeignKey(Section, verbose_name=u'Раздел товаров')
    inner_id = models.CharField(u'Внутренний id', max_length=255, null=True, blank=True)
    name = models.CharField(u'Название модели продукта', max_length=255, unique=True)
    search_name = models.CharField(u'Название для поиска(только бренд и название модели)', max_length=255, blank=True,
                                   null=True)
    code = models.CharField(verbose_name=u'Артикул', max_length=255, blank=True, null=True)
    barcode = models.CharField(verbose_name=u'Штрих код', max_length=255, blank=True, null=True)
    description = models.TextField(u'Краткое описание')
    slug = models.SlugField(u'Slug', max_length=255, unique=True)

    price_min = models.FloatField(verbose_name=u'Минимальная цена', blank=True, null=True, default=0)
    price_max = models.FloatField(verbose_name=u'Максимальная цена', blank=True, null=True, default=0)

    image = models.ImageField(verbose_name=u'Изображение', max_length=255, upload_to=get_section_path,
                              blank=True, null=True)
    image2 = models.ImageField(verbose_name=u'Изображение 2', upload_to=get_section_path, blank=True,
                               null=True)
    image3 = models.ImageField(verbose_name=u'Изображение 3', upload_to=get_section_path, blank=True,
                               null=True)
    image4 = models.ImageField(verbose_name=u'Изображение 4', upload_to=get_section_path, blank=True,
                               null=True)
    image5 = models.ImageField(verbose_name=u'Изображение 5', upload_to=get_section_path, blank=True,
                               null=True)

    video = models.URLField(u'Ссылка на видео', max_length=255, null=True, blank=True)

    votes = models.IntegerField(u'Количество голосов', default=0)
    total_score = models.IntegerField(u'Всего баллов', default=0)
    rating = models.FloatField(u'Рейтинг', default=0)

    items = models.ManyToManyField(Item, verbose_name=u'Идентичные товары', through='ProductModelItemConnection')
    count = models.IntegerField(u'Количество идентичных товаров', default=0)

    feature_group = models.ManyToManyField(FeatureGroup, blank=True)
    # features_icecat = models.ManyToManyField(FeatureIcecat, verbose_name=u'Характеристики',
                                             # through='FeatureIcecatProductConnection')
    bad = models.BooleanField(u'Ошибка привязки товаров', default=False)
    alternative_connections = models.BooleanField(u'Поиск по полю Название для поиска', default=False)
    is_new = models.BooleanField(u'Актуальный товар', default=False)
    # features = models.ManyToManyField(Feature, verbose_name=u'Характеристики', through='FeatureParameterProductConnection')
    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return "/section/{1}".format(self.section.get_slug(),self.slug)

    def is_long_description(self):
        if len(self.description) > 200:
            return True
        return False

    def get_image(self):
        if self.image:
            return u'<img width="100" src="/media/%s" />' % self.image
        return 'no image'

    def get_section(self):
        return ('product_model')

    get_image.allow_tags = True
    get_image.short_description = u'Картинка'

    class Meta:
        verbose_name = u'Модель продукта'
        verbose_name_plural = u'Модели продуктов'


class ProductModelItemConnection(models.Model):
    product_model = models.ForeignKey(ProductModel)
    item = models.ForeignKey(Item)


class FeatureParameterProductConnection(models.Model):
    product = models.ForeignKey(ProductModel)
    feature = models.ForeignKey(Feature, verbose_name=u'Характеристика')
    parameter = models.ForeignKey(Parameter, verbose_name=u'Значение параметра')

    class Meta:
        verbose_name = u'Характеристика для модели продукта'
        verbose_name_plural = u'Характеристики для модели продукта'

class FeatureIcecatProductConnection(models.Model):
    product = models.ForeignKey(ProductModel, verbose_name=u'Товар',related_name='features_icecat')
    group = models.ForeignKey(FeatureGroup, verbose_name=u'Группа характеристик', blank = True, null = True)
    feature = models.ForeignKey(FeatureIcecat, verbose_name=u'Характеристика')
    value = models.CharField(max_length=255)
    
    def __unicode__(self):
        return u'%s' % self.feature


    class Meta:
        verbose_name = u'Характеристика Icecat для модели продукта'
        verbose_name_plural = u'Характеристики Icecat для модели продукта'


########### SIGNALS #########

def section_signal(sender, instance, created, **kwargs):
    if instance.parent and instance.deleted is False:
        parent = Section.objects.get(pk=instance.parent.pk)
        parent.have_child = True
        parent.save()
    # fake delete
    if instance.parent and instance.deleted is True:
        parent = Section.objects.get(pk=instance.parent.pk)
        if Section.objects.filter(parent=parent).count() < 2:
            parent.have_child = False
            parent.save()

    # re-cache category
    if instance.parent:
        cache_parent_key = get_cache_parent_key(instance.parent.id)
        cache.delete(cache_parent_key)
        cache.set(cache_parent_key, instance.parent.get_children_from_parent(), CACHE_TIMEOUT_CATEGORY)


post_save.connect(section_signal, sender=Section)
