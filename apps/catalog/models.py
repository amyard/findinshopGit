# -*- coding: utf-8 -*-

import os
import urllib2
import mimetypes
from django.conf import settings
from django.db import models
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, pre_delete

from utils2 import fields
from utils.upload import get_section_path
from utils2.enum_choices import EnumChoices
from utils2.fields import ContentTypeRestrictedFileField

from categories.models import CategoryBase
from apps.account.models import ExtendedProfile
from apps.section.managers import CurrentManager, FullManager
from .static_names import Color


def is_url_image(url):
    mimetype, encoding = mimetypes.guess_type(url)
    return (mimetype and mimetype.startswith('image'))


def check_url(url):
    try:
        headers = {
            "Range": "bytes=0-10",
            "User-Agent": "MyTestAgent",
            "Accept": "*/*"
        }
        req = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(req)
        return response.code in range(200, 209)
    except Exception, ex:
        return False


class CurrencyRate(models.Model):
    catalog = models.ForeignKey('Catalog')
    name = models.CharField(verbose_name=u'Валюта', max_length=4)
    rate = models.FloatField(verbose_name=u'Курс', null=True)

    class Meta:
        unique_together = ('catalog', 'name')

    def __unicode__(self):
        return u'%s - %s' % (self.catalog, self.name)


class Catalog(models.Model):
    COUNTRIES = EnumChoices((
        (0, u'Украина', 'UA'),
        (1, u'Россия', 'RU'),
        (2, u'Белоруссия', 'BY'),
    ))
    CURRENCIES = EnumChoices((
        (0, u'грн (UAH)', 'UAH'),
        (1, u'руб (RUB)', 'RUB'),
        (2, u'руб (BYR)', 'BYR'),
    ))
    CATALOG_STATE = ((
        (0, u'Создан'),
        (1, u'Обрабатывается'),
        (2, u'Очищен'),
    ))
    website = models.OneToOneField('website.Website')
    country = models.IntegerField(verbose_name=u'Страна', choices=COUNTRIES, default=0)
    rate = models.FloatField(verbose_name=u'Курс валюты', blank=True, null=True)
    currency = models.IntegerField(verbose_name=u'Валюта', choices=CURRENCIES, default=0)
    state = models.IntegerField(verbose_name=u'Состояние', choices=CATALOG_STATE, default=0)

    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'

    def __unicode__(self):
        return u'Каталог для %s' % self.website if self.website else None


class Category(CategoryBase):
    inner_id = models.CharField(
        verbose_name=u'Код категории', max_length=200, blank=True, null=True)
    parrent_inner_id = models.CharField(
        verbose_name=u'Родительский код категории',
        max_length=200, blank=True, null=True)
    catalog = models.ForeignKey(Catalog)
    image = models.ImageField(
        verbose_name=u'Изображение',
        upload_to=get_section_path, blank=True, null=True)
    parameters = fields.JSONField(blank=True, null=True)
    description = models.TextField(
        verbose_name=u'Описание', validators=[MaxLengthValidator(200)],
        blank=True, null=True)
    deleted = models.BooleanField(u'Удален?', default=False)

    objects = CurrentManager()
    full = FullManager()

    class Meta:
        ordering = ["name", "catalog"]
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'

    def get_section(self):
        return ('category_images')

    def get_image_url(self):
        if self.image:
            return self.image.path.replace(
                settings.MEDIA_ROOT + '/', settings.MEDIA_URL)

    def get_image_thumb50_url(self):
        if self.image:
            filename = self.image.path.replace(
                os.path.dirname(self.image.path) + '/', '')
            thumb_filename = filename  # .replace('.', '_50.')
            thumb_path = self.image.path.replace(filename, thumb_filename)
            return thumb_path.replace(
                settings.MEDIA_ROOT + '/', settings.MEDIA_URL)

    def get_all_children(self):
        """
        Returns all child categories of the category.
        """

        def _get_all_children(category, children):
            for category in Category.objects.filter(parent=category.id):
                children.append(category)
                _get_all_children(category, children)

        children = []
        for category in Category.objects.filter(parent=self.id):
            children.append(category)
            _get_all_children(category, children)

        return children

    def get_all_products(self):
        """
        Returns the direct products and all products of the sub categories
        """

        categories = [self]
        categories.extend(self.get_all_children())

        products = Item.objects.defer('description').distinct().filter(
            category__in=categories).distinct()

        return products

    def __unicode__(self):
        return self.name


class Vendor(models.Model):
    """
    Vendor of products
    """
    name = models.CharField(
        u'Название',
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(null=True, blank=True)

    def __unicode__(self):
        return unicode(self.name)


class Item(models.Model):
    STATUS = EnumChoices((
        (0, u'Нет в наличии', 'OUT_OF_STOCK'),
        (1, u'Есть в наличии', 'IN_STOCK'),
        (2, u'Под заказ', 'ON_REQUEST'),
    ))
    GENDER = EnumChoices((
        ('0', u'Не указан', u'Not set'),
        ('1', u'Мужской', u'мужской'),
        ('2', u'Женский', u'женский'),
    ))
    site = models.ForeignKey(
        'website.Website', verbose_name=u'Сайт', blank=True, null=True)

    inner_id = models.CharField(
        verbose_name=u'Код товара', max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, verbose_name=u'Категория')
    code = models.CharField(
        verbose_name=u'Артикул', max_length=500, blank=True, null=True)
    vendor = models.ForeignKey(
        Vendor, verbose_name=u'Производитель', blank=True, null=True)
    name = models.CharField(verbose_name=u'Наименование', max_length=4000)
    description = models.TextField(
        verbose_name=u'Описание', blank=True, null=True)
    color = models.CharField(
        blank=True, null=True, max_length=255, verbose_name=u'Цвет')
    url = models.URLField(
        verbose_name=u'Страница в магазине',
        max_length=4000, blank=True, null=True)
    image_url = models.URLField(
        verbose_name=u'Ссылка на изображение',
        max_length=4000, blank=True, null=True)
    image = models.ImageField(
        verbose_name=u'Изображение',
        upload_to=get_section_path, blank=True, null=True)
    image_alt = models.CharField(
        u'Описание картинки(alt)', max_length=255, blank=True, null=True)
    image1 = models.ImageField(
        verbose_name=u'Изображение 1',
        upload_to=get_section_path, blank=True, null=True)
    image_alt_1 = models.CharField(
        u'Описание картинки 1(alt)', max_length=255, blank=True, null=True)
    image2 = models.ImageField(
        verbose_name=u'Изображение 2',
        upload_to=get_section_path, blank=True, null=True)
    image_alt_2 = models.CharField(
        u'Описание картинки 2(alt)', max_length=255, blank=True, null=True)

    image3 = models.ImageField(
        verbose_name=u'Изображение 3',
        upload_to=get_section_path, blank=True, null=True)
    image_alt_3 = models.CharField(
        u'Описание картинки 3(alt)', max_length=255, blank=True, null=True)

    point = models.ManyToManyField(
        'website.Point', verbose_name=u'Магазин', blank=True)

    price = models.FloatField(verbose_name=u'Цена', blank=True, null=True)
    currency = models.CharField(
        verbose_name=u'Код валюты',
        max_length=5, blank=True, null=True,
        help_text=u"Например UAH, USD, RUB, BYR и т.д.")

    priceRUAH = models.FloatField(
        verbose_name=u'Розница, грн', blank=True, null=True)
    priceRUSD = models.FloatField(
        verbose_name=u'Розница, $', blank=True, null=True)
    priceOUSD = models.FloatField(
        verbose_name=u'Опт, $', blank=True, null=True)
    stock = models.IntegerField(
        verbose_name=u'Наличие товара', choices=STATUS, default=1)
    bestseller = models.BooleanField(verbose_name=u'Бестселлер', default=False)
    discount = models.IntegerField(
        verbose_name=u'Скидка, %', blank=True, null=True)
    wholesale = models.BooleanField(
        verbose_name=u'Оптовая продажа', default=False,
        help_text="Установите отметку, если возможна оптовая продажа")
    guarantee = models.IntegerField(
        verbose_name=u'Гарантийный срок', blank=True, null=True)
    parameters = fields.JSONField(blank=True, null=True)
    image_count = models.IntegerField(
        verbose_name=u'Количество изображений', blank=True, null=True)
    video_count = models.IntegerField(
        verbose_name=u'Количество видео', blank=True, null=True)
    keywords = models.CharField(
        verbose_name=u'Ключевые слова', max_length=400, blank=True, null=True)
    hit_counter = models.IntegerField(
        verbose_name=u'Счетчик просмотров', null=True, blank=True, default=0)
    click_cost = models.FloatField(u'Стоимость клика', default=0)
    one_c = models.BooleanField(u'Реальный товар 1С', default=False)
    delivery = models.BooleanField(u'Доставка', default=False)
    pickup = models.BooleanField(u'Самовывоз', default=False)
    store = models.BooleanField(u'Наличие точки продажи', default=False)
    gender = models.CharField(
        choices=GENDER,
        max_length=2,
        default='0'
    )

    class Meta:
        ordering = ["-click_cost", "site", "name", "category"]
        verbose_name = u'Product'
        verbose_name_plural = u'Products'

    def get_section(self):
        return ('catalog_items')

    def get_url(self):
        if self.url:
            return self.url
        else:
            return 'http://%s/w/ip/%s/' % (self.site, self.id)

    def get_currency(self):
        return Catalog.CURRENCIES.get_title(self.category.catalog.currency)

    def get_phone(self):
        if self.site.user.profile.phone_number:
            return self.site.user.profile.phone_number
        else:
            return ''

    def get_phone_call_center(self):
        if self.site.phone_call_center:
            return self.site.phone_call_center
        else:
            return ''

    def get_image_url(self):
        img_url = u'%simg/no_image.png' % settings.STATIC_URL
        if self.image_url:  # and is_url_image(self.image_url) and check_url(self.image_url):
            img_url = self.image_url
        elif self.image:
            img_url = self.image.url
        return img_url

    def get_price(self):
        discount = self.discount or 0
        price = self.price or 0
        try:
            currency_rate = CurrencyRate.objects.get(catalog=self.category.catalog, name=self.currency).rate
        except ObjectDoesNotExist:
            currency_rate = 1
        currency_setting = CurrencySetting.objects.filter(site=self.site)
        if currency_setting:
            currency_rate = currency_setting[0].rate
        # if self.category.catalog.rate and self.priceRUSD:
        #    return self.priceRUSD * self.category.catalog.rate * (100 - discount) / 100
        # elif not self.category.catalog.rate and not self.price:
        #    return 0
        # else:
        price = price * currency_rate * (100 - discount) / 100
        return "%.2f" % price

    def get_old_price(self):
        discount = self.discount or 0
        old_price = float(self.get_price()) * 100 / (100 - discount)
        return "%.2f" % old_price
        # if self.category.catalog.rate and self.priceRUSD and not self.priceRUAH:
        #    return self.priceRUSD * self.category.catalog.rate
        # elif not self.priceRUAH and not self.priceRUSD:
        #    return 0
        # else:
        #    return self.priceRUAH

    def __unicode__(self):
        return self.name

    @property
    def get_color(self):
        if self.color:
            return [Color.get_name(item) for item in self.color.split(',')]
        return

    def get_ExtendedProfile(self):
        data = ExtendedProfile.objects.filter(user=self.site.user).values(
            'store_name',
            'delivery',
            'credit_sale',
            'payment_methods',
            'nds',
            'wholesale_trade',
            'store_address'
        )
        return data

    def is_long_description(self):
        if len(self.description) > 200:
            return True
        return False


class ItemImage(models.Model):
    image = models.ImageField(verbose_name=u'Изображение товара', upload_to=get_section_path, blank=True,
                              null=True)
    item = models.ForeignKey(Item)

    class Meta:
        verbose_name = u'Изображения товара'
        verbose_name_plural = u'Изображения товаров'

    def get_section(self):
        return ('item_images')

    def __unicode__(self):
        return u'Картинка для %s' % self.item


class ItemVideo(models.Model):
    url = models.URLField(verbose_name=u'Ссылка на видео', blank=True, null=True)
    item = models.ForeignKey(Item)

    class Meta:
        verbose_name = u'Видео товара'
        verbose_name_plural = u'Видео товаров'

    def __unicode__(self):
        return u'Видео для %s' % self.item


class ImportTask(models.Model):
    PRIMARY_FIELDS = EnumChoices((
        (0, u'Код товара', 'INNER_ID'),
        (1, u'Артикул товара', 'CODE'),
    ))
    FORMATS = EnumChoices((
        (0, u'XML (Hotline)', 'XML_HOTLINE'),
        (1, u'YML (Yandex.Market)', 'YML'),
        (2, u'MS Excel', 'XLS'),
        (3, u'XML (Hotprice)', 'XML_HOTPRICE'),
        (4, u'1C', 'ONE_C'),
    ))
    STATUS = EnumChoices((
        (0, u'Принят', 'NEW'),
        (1, u'Обрабатывается', 'PROCESSING'),
        (2, u'Выполнен', 'DONE'),
        (3, u'Ошибка выполнения', 'ERROR'),
        (4, u'Приостановлен', 'STOPED'),

    ))
    # Parameters
    data = ContentTypeRestrictedFileField(
        verbose_name=u'Импортируемый файл',
        upload_to=get_section_path,
        content_types=['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                       'text/xml', 'application/xml'],
        max_upload_size=94371840,
        blank=True,
        null=True
    )
    url = models.URLField(verbose_name=u'Внешняя ссылка', max_length=255, blank=True, null=True)
    validity = models.BooleanField(verbose_name=u'URL проверен', default=False)
    catalog = models.ForeignKey(Catalog, verbose_name=u'Каталог')
    site = models.ForeignKey('website.Website', verbose_name=u'Сайт', blank=True, null=True)
    pid = models.IntegerField(verbose_name=u'Первичный идентификатор', choices=PRIMARY_FIELDS, default=0)
    format = models.IntegerField(verbose_name=u'Формат данных', choices=FORMATS, default=0)
    # Info
    status = models.IntegerField(verbose_name=u'Статус задания', choices=STATUS, default=0)
    start = models.DateTimeField(verbose_name=u'Начало выполнения', blank=True, null=True)
    complete = models.DateTimeField(verbose_name=u'Конец выполнения', blank=True, null=True)
    error = models.TextField(verbose_name=u'Код ошибки', blank=True, null=True)
    # Counters
    items_processed = models.IntegerField(verbose_name=u'Обработано товаров', blank=True, null=True)
    items_updated = models.IntegerField(verbose_name=u'Обновлено товаров', blank=True, null=True)
    items_ignored = models.IntegerField(verbose_name=u'Игнорировано товаров', blank=True, null=True)

    def get_section(self):
        return ('import_task_data')

    class Meta:
        verbose_name = u'Задание импорта'
        verbose_name_plural = u'Задания импорта'

    def __unicode__(self):
        return u'Импорт в %s' % self.catalog


class ExportTask(models.Model):
    STATUS = EnumChoices((
        (0, u'Принят', 'NEW'),
        (1, u'Выполняется', 'PROCESSING'),
        (2, u'Выполнен', 'DONE'),
        (3, u'Ошибка', 'ERROR'),
    ))
    data = models.FileField(verbose_name=u'Экспортируемый файл', upload_to=get_section_path,
                            blank=True, null=True)
    catalog = models.ForeignKey(Catalog, verbose_name=u'Каталог')
    site = models.ForeignKey('website.Website', verbose_name=u'Сайт', blank=True, null=True)
    status = models.IntegerField(verbose_name=u'Статус задания', choices=STATUS, default=0)
    start = models.DateTimeField(verbose_name=u'Начало выполнения', blank=True, null=True)
    complete = models.DateTimeField(verbose_name=u'Конец выполнения', blank=True, null=True)
    error = models.TextField(verbose_name=u'Код ошибки', blank=True, null=True)

    class Meta:
        verbose_name = u'Задание экспорта'
        verbose_name_plural = u'Задания экспорта'
    
    def get_section(self):
        return ('export_task_data')

    def __unicode__(self):
        return u'Экспорт из %s' % self.catalog


class Order(models.Model):
    STATUS = EnumChoices((
        (0, u'Принят', 'ACCEPTED'),
        (1, u'Обрабатывается', 'PROCESSING'),
        (2, u'Отменен', 'DECLINED'),
        (3, u'Подтвержден', 'APPROOVED'),
        (4, u'Отправлен', 'SENT'),
    ))
    catalog = models.ForeignKey(Catalog)
    number = models.CharField(verbose_name=u'Номер заказа', max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    status = models.IntegerField(verbose_name=u'Статус', choices=STATUS, default=0)
    contact = models.CharField(verbose_name=u'Контакт', max_length=250)
    phone = models.CharField(verbose_name=u'Номер телефона', max_length=50)
    email = models.EmailField(verbose_name=u'Email')
    description = models.TextField(verbose_name=u'Примечания', blank=True, null=True)
    cost = models.FloatField(verbose_name=u'Стоимость заказа')

    class Meta:
        ordering = ["number"]
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_status_key(self):
        return self.STATUS.get_name(self.status)

    def get_status_title(self):
        return self.STATUS.get_title(self.status)

    def __unicode__(self):
        return u'Заказ №%s от %s по каталогу %s' % (self.number, self.created_date, self.catalog.website)


class OrderItem(models.Model):
    class Meta:
        verbose_name = u'Заказанный товар'
        verbose_name_plural = u'Заказанные товары'

    order = models.ForeignKey(Order, verbose_name=u'Заказ')
    item = models.ForeignKey(Item, verbose_name=u'Товар')
    quantity = models.IntegerField(verbose_name=u'Количество')
    cost = models.FloatField(u'Цена')

    def __unicode__(self):
        return u'Товар для %s' % self.order


class CurrencySetting(models.Model):
    CURRENCY_CHOICES = (
        (0, 'UAH'),
        (1, 'RUB'),
        (2, 'USD'),
        (3, 'EUR'),
        (4, 'BYR'),
    )
    site = models.ForeignKey('website.Website', verbose_name=u'Сайт')
    currency = models.SmallIntegerField(u'Валюта', choices=CURRENCY_CHOICES, default=CURRENCY_CHOICES[0][0])
    rate = models.FloatField(u'Курс по отношению к UAH', default=1.0)


from signals import *

'''     rt_field = name
    rt_field = color
    rt_field = currency
    rt_attr_float = price
    rt_field = category_name
    rt_field = image_url
    rt_field = gender
    rt_attr_multi = point_ids
    rt_attr_uint = vendor_id
    rt_attr_uint = site_type
    rt_attr_float = click_cost

    rt_attr_bool = delivery
    rt_attr_bool = store
    rt_attr_bool = pickup
    rt_attr_bool = one_c
'''



def clear_item(instance, **kwargs):
    for item in Item.objects.filter(site_id=instance.site_id):
        item.price = 0
        item.save()

# post_save.connect(rt_index_update, sender=Item)
pre_delete.connect(clear_item, sender=ImportTask)
