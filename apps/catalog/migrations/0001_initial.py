# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields
import utils2.fields
import utils.upload
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', models.IntegerField(default=0, verbose_name='\u0421\u0442\u0440\u0430\u043d\u0430', choices=[(0, '\u0423\u043a\u0440\u0430\u0438\u043d\u0430'), (1, '\u0420\u043e\u0441\u0441\u0438\u044f'), (2, '\u0411\u0435\u043b\u043e\u0440\u0443\u0441\u0441\u0438\u044f')])),
                ('rate', models.FloatField(null=True, verbose_name='\u041a\u0443\u0440\u0441 \u0432\u0430\u043b\u044e\u0442\u044b', blank=True)),
                ('currency', models.IntegerField(default=0, verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430', choices=[(0, '\u0433\u0440\u043d (UAH)'), (1, '\u0440\u0443\u0431 (RUB)'), (2, '\u0440\u0443\u0431 (BYR)')])),
                ('state', models.IntegerField(default=0, verbose_name='\u0421\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435', choices=[(0, '\u0421\u043e\u0437\u0434\u0430\u043d'), (1, '\u041e\u0431\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u0435\u0442\u0441\u044f'), (2, '\u041e\u0447\u0438\u0449\u0435\u043d')])),
                ('website', models.OneToOneField(to='website.Website')),
            ],
            options={
                'verbose_name': '\u041a\u0430\u0442\u0430\u043b\u043e\u0433',
                'verbose_name_plural': '\u041a\u0430\u0442\u0430\u043b\u043e\u0433\u0438',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('inner_id', models.CharField(max_length=200, null=True, verbose_name='\u041a\u043e\u0434 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438', blank=True)),
                ('parrent_inner_id', models.CharField(max_length=200, null=True, verbose_name='\u0420\u043e\u0434\u0438\u0442\u0435\u043b\u044c\u0441\u043a\u0438\u0439 \u043a\u043e\u0434 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438', blank=True)),
                ('image', models.ImageField(upload_to=utils.upload.get_section_path, null=True, verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435', blank=True)),
                ('parameters', utils2.fields.JSONField(null=True, blank=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', validators=[django.core.validators.MaxLengthValidator(200)])),
                ('deleted', models.BooleanField(default=False, verbose_name='\u0423\u0434\u0430\u043b\u0435\u043d?')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('catalog', models.ForeignKey(to='catalog.Catalog')),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', verbose_name='parent', blank=True, to='catalog.Category', null=True)),
            ],
            options={
                'ordering': ['name', 'catalog'],
                'verbose_name': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f',
                'verbose_name_plural': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438',
            },
        ),
        migrations.CreateModel(
            name='CurrencyRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=4, verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430')),
                ('rate', models.FloatField(null=True, verbose_name='\u041a\u0443\u0440\u0441')),
                ('catalog', models.ForeignKey(to='catalog.Catalog')),
            ],
        ),
        migrations.CreateModel(
            name='CurrencySetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('currency', models.SmallIntegerField(default=0, verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430', choices=[(0, b'UAH'), (1, b'RUB'), (2, b'USD'), (3, b'EUR'), (4, b'BYR')])),
                ('rate', models.FloatField(default=1.0, verbose_name='\u041a\u0443\u0440\u0441 \u043f\u043e \u043e\u0442\u043d\u043e\u0448\u0435\u043d\u0438\u044e \u043a UAH')),
                ('site', models.ForeignKey(verbose_name='\u0421\u0430\u0439\u0442', to='website.Website')),
            ],
        ),
        migrations.CreateModel(
            name='ExportTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.FileField(upload_to=utils.upload.get_section_path, null=True, verbose_name='\u042d\u043a\u0441\u043f\u043e\u0440\u0442\u0438\u0440\u0443\u0435\u043c\u044b\u0439 \u0444\u0430\u0439\u043b', blank=True)),
                ('status', models.IntegerField(default=0, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441 \u0437\u0430\u0434\u0430\u043d\u0438\u044f', choices=[(0, '\u041f\u0440\u0438\u043d\u044f\u0442'), (1, '\u0412\u044b\u043f\u043e\u043b\u043d\u044f\u0435\u0442\u0441\u044f'), (2, '\u0412\u044b\u043f\u043e\u043b\u043d\u0435\u043d'), (3, '\u041e\u0448\u0438\u0431\u043a\u0430')])),
                ('start', models.DateTimeField(null=True, verbose_name='\u041d\u0430\u0447\u0430\u043b\u043e \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f', blank=True)),
                ('complete', models.DateTimeField(null=True, verbose_name='\u041a\u043e\u043d\u0435\u0446 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f', blank=True)),
                ('error', models.TextField(null=True, verbose_name='\u041a\u043e\u0434 \u043e\u0448\u0438\u0431\u043a\u0438', blank=True)),
                ('catalog', models.ForeignKey(verbose_name='\u041a\u0430\u0442\u0430\u043b\u043e\u0433', to='catalog.Catalog')),
                ('site', models.ForeignKey(verbose_name='\u0421\u0430\u0439\u0442', blank=True, to='website.Website', null=True)),
            ],
            options={
                'verbose_name': '\u0417\u0430\u0434\u0430\u043d\u0438\u0435 \u044d\u043a\u0441\u043f\u043e\u0440\u0442\u0430',
                'verbose_name_plural': '\u0417\u0430\u0434\u0430\u043d\u0438\u044f \u044d\u043a\u0441\u043f\u043e\u0440\u0442\u0430',
            },
        ),
        migrations.CreateModel(
            name='ImportTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', utils2.fields.ContentTypeRestrictedFileField(upload_to=utils.upload.get_section_path, null=True, verbose_name='\u0418\u043c\u043f\u043e\u0440\u0442\u0438\u0440\u0443\u0435\u043c\u044b\u0439 \u0444\u0430\u0439\u043b', blank=True)),
                ('url', models.URLField(max_length=255, null=True, verbose_name='\u0412\u043d\u0435\u0448\u043d\u044f\u044f \u0441\u0441\u044b\u043b\u043a\u0430', blank=True)),
                ('validity', models.BooleanField(verbose_name='URL \u043f\u0440\u043e\u0432\u0435\u0440\u0435\u043d')),
                ('pid', models.IntegerField(default=0, verbose_name='\u041f\u0435\u0440\u0432\u0438\u0447\u043d\u044b\u0439 \u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440', choices=[(0, '\u041a\u043e\u0434 \u0442\u043e\u0432\u0430\u0440\u0430'), (1, '\u0410\u0440\u0442\u0438\u043a\u0443\u043b \u0442\u043e\u0432\u0430\u0440\u0430')])),
                ('format', models.IntegerField(default=0, verbose_name='\u0424\u043e\u0440\u043c\u0430\u0442 \u0434\u0430\u043d\u043d\u044b\u0445', choices=[(0, 'XML (Hotline)'), (1, 'YML (Yandex.Market)'), (2, 'MS Excel'), (3, 'XML (Hotprice)'), (4, '1C')])),
                ('status', models.IntegerField(default=0, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441 \u0437\u0430\u0434\u0430\u043d\u0438\u044f', choices=[(0, '\u041f\u0440\u0438\u043d\u044f\u0442'), (1, '\u041e\u0431\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u0435\u0442\u0441\u044f'), (2, '\u0412\u044b\u043f\u043e\u043b\u043d\u0435\u043d'), (3, '\u041e\u0448\u0438\u0431\u043a\u0430 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f'), (4, '\u041f\u0440\u0438\u043e\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d')])),
                ('start', models.DateTimeField(null=True, verbose_name='\u041d\u0430\u0447\u0430\u043b\u043e \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f', blank=True)),
                ('complete', models.DateTimeField(null=True, verbose_name='\u041a\u043e\u043d\u0435\u0446 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f', blank=True)),
                ('error', models.TextField(null=True, verbose_name='\u041a\u043e\u0434 \u043e\u0448\u0438\u0431\u043a\u0438', blank=True)),
                ('items_processed', models.IntegerField(null=True, verbose_name='\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u0430\u043d\u043e \u0442\u043e\u0432\u0430\u0440\u043e\u0432', blank=True)),
                ('items_updated', models.IntegerField(null=True, verbose_name='\u041e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u043e \u0442\u043e\u0432\u0430\u0440\u043e\u0432', blank=True)),
                ('items_ignored', models.IntegerField(null=True, verbose_name='\u0418\u0433\u043d\u043e\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u043e \u0442\u043e\u0432\u0430\u0440\u043e\u0432', blank=True)),
                ('catalog', models.ForeignKey(verbose_name='\u041a\u0430\u0442\u0430\u043b\u043e\u0433', to='catalog.Catalog')),
                ('site', models.ForeignKey(verbose_name='\u0421\u0430\u0439\u0442', blank=True, to='website.Website', null=True)),
            ],
            options={
                'verbose_name': '\u0417\u0430\u0434\u0430\u043d\u0438\u0435 \u0438\u043c\u043f\u043e\u0440\u0442\u0430',
                'verbose_name_plural': '\u0417\u0430\u0434\u0430\u043d\u0438\u044f \u0438\u043c\u043f\u043e\u0440\u0442\u0430',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inner_id', models.CharField(max_length=200, null=True, verbose_name='\u041a\u043e\u0434 \u0442\u043e\u0432\u0430\u0440\u0430', blank=True)),
                ('code', models.CharField(max_length=500, null=True, verbose_name='\u0410\u0440\u0442\u0438\u043a\u0443\u043b', blank=True)),
                ('name', models.CharField(max_length=4000, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435')),
                ('description', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('color', models.CharField(max_length=255, null=True, verbose_name='\u0426\u0432\u0435\u0442', blank=True)),
                ('url', models.URLField(max_length=4000, null=True, verbose_name='\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430 \u0432 \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u0435', blank=True)),
                ('image_url', models.URLField(max_length=4000, null=True, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435', blank=True)),
                ('image', models.ImageField(upload_to=utils.upload.get_section_path, null=True, verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435', blank=True)),
                ('image_alt', models.CharField(max_length=255, null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0438(alt)', blank=True)),
                ('image1', models.ImageField(upload_to=utils.upload.get_section_path, null=True, verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 1', blank=True)),
                ('image_alt_1', models.CharField(max_length=255, null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0438 1(alt)', blank=True)),
                ('image2', models.ImageField(upload_to=utils.upload.get_section_path, null=True, verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 2', blank=True)),
                ('image_alt_2', models.CharField(max_length=255, null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0438 2(alt)', blank=True)),
                ('image3', models.ImageField(upload_to=utils.upload.get_section_path, null=True, verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 3', blank=True)),
                ('image_alt_3', models.CharField(max_length=255, null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0438 3(alt)', blank=True)),
                ('price', models.FloatField(null=True, verbose_name='\u0426\u0435\u043d\u0430', blank=True)),
                ('currency', models.CharField(help_text='\u041d\u0430\u043f\u0440\u0438\u043c\u0435\u0440 UAH, USD, RUB, BYR \u0438 \u0442.\u0434.', max_length=5, null=True, verbose_name='\u041a\u043e\u0434 \u0432\u0430\u043b\u044e\u0442\u044b', blank=True)),
                ('priceRUAH', models.FloatField(null=True, verbose_name='\u0420\u043e\u0437\u043d\u0438\u0446\u0430, \u0433\u0440\u043d', blank=True)),
                ('priceRUSD', models.FloatField(null=True, verbose_name='\u0420\u043e\u0437\u043d\u0438\u0446\u0430, $', blank=True)),
                ('priceOUSD', models.FloatField(null=True, verbose_name='\u041e\u043f\u0442, $', blank=True)),
                ('stock', models.IntegerField(default=1, verbose_name='\u041d\u0430\u043b\u0438\u0447\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430', choices=[(0, '\u041d\u0435\u0442 \u0432 \u043d\u0430\u043b\u0438\u0447\u0438\u0438'), (1, '\u0415\u0441\u0442\u044c \u0432 \u043d\u0430\u043b\u0438\u0447\u0438\u0438'), (2, '\u041f\u043e\u0434 \u0437\u0430\u043a\u0430\u0437')])),
                ('bestseller', models.BooleanField(default=False, verbose_name='\u0411\u0435\u0441\u0442\u0441\u0435\u043b\u043b\u0435\u0440')),
                ('discount', models.IntegerField(null=True, verbose_name='\u0421\u043a\u0438\u0434\u043a\u0430, %', blank=True)),
                ('wholesale', models.BooleanField(default=False, help_text=b'\xd0\xa3\xd1\x81\xd1\x82\xd0\xb0\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xb8\xd1\x82\xd0\xb5 \xd0\xbe\xd1\x82\xd0\xbc\xd0\xb5\xd1\x82\xd0\xba\xd1\x83, \xd0\xb5\xd1\x81\xd0\xbb\xd0\xb8 \xd0\xb2\xd0\xbe\xd0\xb7\xd0\xbc\xd0\xbe\xd0\xb6\xd0\xbd\xd0\xb0 \xd0\xbe\xd0\xbf\xd1\x82\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x8f \xd0\xbf\xd1\x80\xd0\xbe\xd0\xb4\xd0\xb0\xd0\xb6\xd0\xb0', verbose_name='\u041e\u043f\u0442\u043e\u0432\u0430\u044f \u043f\u0440\u043e\u0434\u0430\u0436\u0430')),
                ('guarantee', models.IntegerField(null=True, verbose_name='\u0413\u0430\u0440\u0430\u043d\u0442\u0438\u0439\u043d\u044b\u0439 \u0441\u0440\u043e\u043a', blank=True)),
                ('parameters', utils2.fields.JSONField(null=True, blank=True)),
                ('image_count', models.IntegerField(null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0439', blank=True)),
                ('video_count', models.IntegerField(null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0432\u0438\u0434\u0435\u043e', blank=True)),
                ('keywords', models.CharField(max_length=400, null=True, verbose_name='\u041a\u043b\u044e\u0447\u0435\u0432\u044b\u0435 \u0441\u043b\u043e\u0432\u0430', blank=True)),
                ('hit_counter', models.IntegerField(default=0, null=True, verbose_name='\u0421\u0447\u0435\u0442\u0447\u0438\u043a \u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440\u043e\u0432', blank=True)),
                ('click_cost', models.FloatField(default=0, verbose_name='\u0421\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c \u043a\u043b\u0438\u043a\u0430')),
                ('one_c', models.BooleanField(default=False, verbose_name='\u0420\u0435\u0430\u043b\u044c\u043d\u044b\u0439 \u0442\u043e\u0432\u0430\u0440 1\u0421')),
                ('delivery', models.BooleanField(default=False, verbose_name='\u0414\u043e\u0441\u0442\u0430\u0432\u043a\u0430')),
                ('pickup', models.BooleanField(default=False, verbose_name='\u0421\u0430\u043c\u043e\u0432\u044b\u0432\u043e\u0437')),
                ('store', models.BooleanField(default=False, verbose_name='\u041d\u0430\u043b\u0438\u0447\u0438\u0435 \u0442\u043e\u0447\u043a\u0438 \u043f\u0440\u043e\u0434\u0430\u0436\u0438')),
                ('gender', models.CharField(default=0, max_length=1, choices=[(0, '\u041d\u0435 \u0443\u043a\u0430\u0437\u0430\u043d'), (1, '\u041c\u0443\u0436\u0441\u043a\u043e\u0439'), (2, '\u0416\u0435\u043d\u0441\u043a\u0438\u0439')])),
                ('category', models.ForeignKey(verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f', to='catalog.Category')),
                ('point', models.ManyToManyField(to='website.Point', verbose_name='\u041c\u0430\u0433\u0430\u0437\u0438\u043d', blank=True)),
                ('site', models.ForeignKey(verbose_name='\u0421\u0430\u0439\u0442', blank=True, to='website.Website', null=True)),
            ],
            options={
                'ordering': ['-click_cost', 'site', 'name', 'category'],
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=utils.upload.get_section_path, null=True, verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430', blank=True)),
                ('item', models.ForeignKey(to='catalog.Item')),
            ],
            options={
                'verbose_name': '\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430',
                'verbose_name_plural': '\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u043e\u0432',
            },
        ),
        migrations.CreateModel(
            name='ItemVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(null=True, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u0432\u0438\u0434\u0435\u043e', blank=True)),
                ('item', models.ForeignKey(to='catalog.Item')),
            ],
            options={
                'verbose_name': '\u0412\u0438\u0434\u0435\u043e \u0442\u043e\u0432\u0430\u0440\u0430',
                'verbose_name_plural': '\u0412\u0438\u0434\u0435\u043e \u0442\u043e\u0432\u0430\u0440\u043e\u0432',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=100, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0437\u0430\u043a\u0430\u0437\u0430')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(default=0, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', choices=[(0, '\u041f\u0440\u0438\u043d\u044f\u0442'), (1, '\u041e\u0431\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u0435\u0442\u0441\u044f'), (2, '\u041e\u0442\u043c\u0435\u043d\u0435\u043d'), (3, '\u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d'), (4, '\u041e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d')])),
                ('contact', models.CharField(max_length=250, verbose_name='\u041a\u043e\u043d\u0442\u0430\u043a\u0442')),
                ('phone', models.CharField(max_length=50, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('description', models.TextField(null=True, verbose_name='\u041f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u044f', blank=True)),
                ('cost', models.FloatField(verbose_name='\u0421\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c \u0437\u0430\u043a\u0430\u0437\u0430')),
                ('catalog', models.ForeignKey(to='catalog.Catalog')),
            ],
            options={
                'ordering': ['number'],
                'verbose_name': '\u0417\u0430\u043a\u0430\u0437',
                'verbose_name_plural': '\u0417\u0430\u043a\u0430\u0437\u044b',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e')),
                ('cost', models.FloatField(verbose_name='\u0426\u0435\u043d\u0430')),
                ('item', models.ForeignKey(verbose_name='\u0422\u043e\u0432\u0430\u0440', to='catalog.Item')),
                ('order', models.ForeignKey(verbose_name='\u0417\u0430\u043a\u0430\u0437', to='catalog.Order')),
            ],
            options={
                'verbose_name': '\u0417\u0430\u043a\u0430\u0437\u0430\u043d\u043d\u044b\u0439 \u0442\u043e\u0432\u0430\u0440',
                'verbose_name_plural': '\u0417\u0430\u043a\u0430\u0437\u0430\u043d\u043d\u044b\u0435 \u0442\u043e\u0432\u0430\u0440\u044b',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('slug', models.SlugField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='vendor',
            field=models.ForeignKey(verbose_name='\u041f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c', blank=True, to='catalog.Vendor', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='currencyrate',
            unique_together=set([('catalog', 'name')]),
        ),
    ]
