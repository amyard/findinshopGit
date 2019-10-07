# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.section.utils


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('admin_name', models.CharField(help_text='\u0414\u043b\u044f \u0440\u0430\u0437\u043b\u0438\u0447\u0438\u044f \u043e\u0434\u0438\u043d\u0430\u043a\u043e\u0432\u044b\u0445 \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a: \u0411\u0440\u0435\u043d\u0434\u044b \u0434\u043b\u044f \u043c\u043e\u0431\u0438\u043b\u044c\u043d\u044b\u0445 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u043e\u0432, \u0411\u0440\u0435\u043d\u0434\u044b \u0434\u043b\u044f \u0430\u0432\u0442\u043e\u043c\u043e\u0431\u0438\u043b\u0435\u0439', max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u0430\u0434\u043c\u0438\u043d\u0430')),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('sort', models.PositiveSmallIntegerField(default=0, verbose_name='\u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442 \u043f\u0440\u0438 \u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0435')),
            ],
            options={
                'verbose_name': '\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0430',
                'verbose_name_plural': '\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='FeatureGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inner_id', models.IntegerField(verbose_name='\u0412\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u0438\u0439 id')),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0413\u0440\u0443\u043f\u043f\u0430 \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438',
                'verbose_name_plural': '\u0413\u0440\u0443\u043f\u043f\u044b \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='FeatureIcecat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inner_id', models.IntegerField(verbose_name='\u0412\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u0438\u0439 id')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435', blank=True)),
            ],
            options={
                'verbose_name': '\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0430 Icecat',
                'verbose_name_plural': '\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438 Icecat',
            },
        ),
        migrations.CreateModel(
            name='FeatureIcecatProductConnection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=255)),
                ('feature', models.ForeignKey(verbose_name='\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0430', to='section.FeatureIcecat')),
                ('group', models.ForeignKey(verbose_name='\u0413\u0440\u0443\u043f\u043f\u0430 \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a', blank=True, to='section.FeatureGroup', null=True)),
            ],
            options={
                'verbose_name': '\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0430 Icecat \u0434\u043b\u044f \u043c\u043e\u0434\u0435\u043b\u0438 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430',
                'verbose_name_plural': '\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438 Icecat \u0434\u043b\u044f \u043c\u043e\u0434\u0435\u043b\u0438 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430',
            },
        ),
        migrations.CreateModel(
            name='FeatureParameterConnection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feature', models.ForeignKey(related_name='parameter_connections', to='section.Feature')),
            ],
            options={
                'verbose_name': '\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u0434\u043b\u044f \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438',
                'verbose_name_plural': '\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u0434\u043b\u044f \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='FeatureParameterProductConnection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feature', models.ForeignKey(verbose_name='\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0430', to='section.Feature')),
            ],
            options={
                'verbose_name': '\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0430 \u0434\u043b\u044f \u043c\u043e\u0434\u0435\u043b\u0438 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430',
                'verbose_name_plural': '\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438 \u0434\u043b\u044f \u043c\u043e\u0434\u0435\u043b\u0438 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430',
            },
        ),
        migrations.CreateModel(
            name='FeatureTypeIcecat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('types', models.CharField(max_length=255, verbose_name='\u0422\u0438\u043f')),
            ],
        ),
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inner_id', models.IntegerField(verbose_name='\u0412\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u0438\u0439 id')),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('sign', models.CharField(max_length=255, verbose_name='\u0417\u043d\u0430\u043a')),
                ('sign_rus', models.CharField(max_length=255, verbose_name='\u0417\u043d\u0430\u043a \u043d\u0430 \u0440\u0443\u0441\u0441\u043a\u043e\u043c')),
            ],
            options={
                'verbose_name': '\u041c\u0435\u0440\u0430',
                'verbose_name_plural': '\u041c\u0435\u0440\u044b',
            },
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('sort', models.PositiveSmallIntegerField(default=0, verbose_name='\u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442 \u043f\u0440\u0438 \u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0435')),
            ],
            options={
                'verbose_name': '\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440',
                'verbose_name_plural': '\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b',
            },
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inner_id', models.CharField(max_length=255, null=True, verbose_name='\u0412\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u0438\u0439 id', blank=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043c\u043e\u0434\u0435\u043b\u0438 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430')),
                ('search_name', models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u043f\u043e\u0438\u0441\u043a\u0430(\u0442\u043e\u043b\u044c\u043a\u043e \u0431\u0440\u0435\u043d\u0434 \u0438 \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043c\u043e\u0434\u0435\u043b\u0438)', blank=True)),
                ('code', models.CharField(max_length=255, null=True, verbose_name='\u0410\u0440\u0442\u0438\u043a\u0443\u043b', blank=True)),
                ('barcode', models.CharField(max_length=255, null=True, verbose_name='\u0428\u0442\u0440\u0438\u0445 \u043a\u043e\u0434', blank=True)),
                ('description', models.TextField(verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug')),
                ('price_min', models.FloatField(default=0, null=True, verbose_name='\u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u0430\u044f \u0446\u0435\u043d\u0430', blank=True)),
                ('price_max', models.FloatField(default=0, null=True, verbose_name='\u041c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u0430\u044f \u0446\u0435\u043d\u0430', blank=True)),
                ('image', models.ImageField(max_length=255, upload_to=apps.section.utils.get_section_path, null=True, verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435', blank=True)),
                ('image2', models.ImageField(upload_to=apps.section.utils.get_section_path, null=True, verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 2', blank=True)),
                ('image3', models.ImageField(upload_to=apps.section.utils.get_section_path, null=True, verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 3', blank=True)),
                ('image4', models.ImageField(upload_to=apps.section.utils.get_section_path, null=True, verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 4', blank=True)),
                ('image5', models.ImageField(upload_to=apps.section.utils.get_section_path, null=True, verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 5', blank=True)),
                ('video', models.URLField(max_length=255, null=True, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u0432\u0438\u0434\u0435\u043e', blank=True)),
                ('votes', models.IntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0433\u043e\u043b\u043e\u0441\u043e\u0432')),
                ('total_score', models.IntegerField(default=0, verbose_name='\u0412\u0441\u0435\u0433\u043e \u0431\u0430\u043b\u043b\u043e\u0432')),
                ('rating', models.FloatField(default=0, verbose_name='\u0420\u0435\u0439\u0442\u0438\u043d\u0433')),
                ('count', models.IntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0438\u0434\u0435\u043d\u0442\u0438\u0447\u043d\u044b\u0445 \u0442\u043e\u0432\u0430\u0440\u043e\u0432')),
                ('bad', models.BooleanField(default=False, verbose_name='\u041e\u0448\u0438\u0431\u043a\u0430 \u043f\u0440\u0438\u0432\u044f\u0437\u043a\u0438 \u0442\u043e\u0432\u0430\u0440\u043e\u0432')),
                ('alternative_connections', models.BooleanField(default=False, verbose_name='\u041f\u043e\u0438\u0441\u043a \u043f\u043e \u043f\u043e\u043b\u044e \u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u043f\u043e\u0438\u0441\u043a\u0430')),
                ('is_new', models.BooleanField(default=False, verbose_name='\u0410\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u044b\u0439 \u0442\u043e\u0432\u0430\u0440')),
                ('feature_group', models.ManyToManyField(to='section.FeatureGroup', blank=True)),
            ],
            options={
                'verbose_name': '\u041c\u043e\u0434\u0435\u043b\u044c \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430',
                'verbose_name_plural': '\u041c\u043e\u0434\u0435\u043b\u0438 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u043e\u0432',
            },
        ),
        migrations.CreateModel(
            name='ProductModelItemConnection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.ForeignKey(to='catalog.Item')),
                ('product_model', models.ForeignKey(to='section.ProductModel')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0440\u0430\u0437\u0434\u0435\u043b\u0430')),
                ('inner_id', models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435', blank=True)),
                ('parse_url', models.CharField(max_length=255, null=True, verbose_name='\u0423\u0440\u043b \u0434\u043b\u044f \u043f\u0430\u0440\u0441\u0438\u043d\u0433\u0430', blank=True)),
                ('icon', models.ImageField(upload_to=apps.section.utils.get_section_path, null=True, verbose_name='\u041b\u043e\u0433\u043e', blank=True)),
                ('thumb', models.ImageField(upload_to=apps.section.utils.get_section_path, null=True, verbose_name='\u041c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430', blank=True)),
                ('description', models.TextField(null=True, verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0440\u0430\u0437\u0434\u0435\u043b\u0430', blank=True)),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('sort', models.PositiveSmallIntegerField(default=0, verbose_name='\u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442 \u043f\u0440\u0438 \u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0435')),
                ('have_child', models.BooleanField(default=False, verbose_name='\u0418\u043c\u0435\u0435\u0442 \u043f\u043e\u0434\u0440\u0430\u0437\u0434\u0435\u043b')),
                ('deleted', models.BooleanField(default=False, verbose_name='\u0423\u0434\u0430\u043b\u0435\u043d?')),
                ('state', models.CharField(blank=True, max_length=255, null=True, verbose_name='', choices=[(0, '\u0421\u043e\u0437\u0434\u0430\u043d'), (1, '\u041e\u0431\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u0435\u0442\u0441\u044f'), (2, '\u041e\u0447\u0438\u0449\u0435\u043d')])),
                ('features', models.ManyToManyField(help_text='\u0422\u043e\u043b\u044c\u043a\u043e \u0434\u043b\u044f \u043a\u0440\u0430\u0439\u043d\u0438\u0445 \u043f\u043e\u0434\u0440\u0430\u0437\u0434\u0435\u043b\u043e\u0432!', to='section.Feature', verbose_name='\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438 \u0434\u043b\u044f \u0440\u0430\u0437\u0434\u0435\u043b\u0430', blank=True)),
                ('parent', models.ForeignKey(verbose_name='\u0420\u043e\u0434\u0438\u0442\u0435\u043b\u044c\u0441\u043a\u0438\u0439 \u0440\u0430\u0437\u0434\u0435\u043b', blank=True, to='section.Section', null=True)),
            ],
            options={
                'verbose_name': '\u0420\u0430\u0437\u0434\u0435\u043b \u0442\u043e\u0432\u0430\u0440\u043e\u0432',
                'verbose_name_plural': '\u0420\u0430\u0437\u0434\u0435\u043b\u044b \u0442\u043e\u0432\u0430\u0440\u043e\u0432',
            },
        ),
        migrations.AddField(
            model_name='productmodel',
            name='items',
            field=models.ManyToManyField(to='catalog.Item', verbose_name='\u0418\u0434\u0435\u043d\u0442\u0438\u0447\u043d\u044b\u0435 \u0442\u043e\u0432\u0430\u0440\u044b', through='section.ProductModelItemConnection'),
        ),
        migrations.AddField(
            model_name='productmodel',
            name='section',
            field=models.ForeignKey(verbose_name='\u0420\u0430\u0437\u0434\u0435\u043b \u0442\u043e\u0432\u0430\u0440\u043e\u0432', to='section.Section'),
        ),
        migrations.AddField(
            model_name='featureparameterproductconnection',
            name='parameter',
            field=models.ForeignKey(verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u0430', to='section.Parameter'),
        ),
        migrations.AddField(
            model_name='featureparameterproductconnection',
            name='product',
            field=models.ForeignKey(to='section.ProductModel'),
        ),
        migrations.AddField(
            model_name='featureparameterconnection',
            name='parameter',
            field=models.ForeignKey(verbose_name='\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u043e\u0442\u043d\u043e\u0441\u044f\u0449\u0438\u0435\u0441\u044f \u043a \u0434\u0430\u043d\u043d\u043e\u0439 \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0435', to='section.Parameter'),
        ),
        migrations.AddField(
            model_name='featureicecatproductconnection',
            name='product',
            field=models.ForeignKey(related_name='features_icecat', verbose_name='\u0422\u043e\u0432\u0430\u0440', to='section.ProductModel'),
        ),
        migrations.AddField(
            model_name='featureicecat',
            name='measure',
            field=models.ForeignKey(blank=True, to='section.Measure', null=True),
        ),
        migrations.AddField(
            model_name='featureicecat',
            name='types',
            field=models.ForeignKey(blank=True, to='section.FeatureTypeIcecat', null=True),
        ),
        migrations.AddField(
            model_name='feature',
            name='parameters',
            field=models.ManyToManyField(related_name='features', through='section.FeatureParameterConnection', to='section.Parameter'),
        ),
    ]
