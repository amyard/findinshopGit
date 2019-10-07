# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CouponSubscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_name', models.CharField(default='\u041d\u0435\u0442 \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u044f \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430', max_length=4000, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435')),
                ('product_group', models.CharField(max_length=150, null=True, verbose_name='\u0413\u0440\u0443\u043f\u043f\u0430 \u0442\u043e\u0432\u0430\u0440\u043e\u0432')),
                ('market_name', models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u0430 \u043a\u043e\u0442\u043e\u0440\u044b\u0439 \u043f\u0440\u0435\u0434\u043e\u0441\u0442\u0430\u0432\u0438\u043b \u043a\u0443\u043f\u043e\u043d')),
                ('price', models.FloatField(null=True, verbose_name='\u0426\u0435\u043d\u0430', blank=True)),
                ('count', models.PositiveSmallIntegerField(default=1, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u0439')),
                ('coupon', models.ForeignKey(to='coupon.Coupon')),
            ],
            options={
                'verbose_name': '\u0417\u0430\u043a\u0430\u0437\u043d\u044b\u0435 \u043a\u0443\u043f\u043e\u043d\u044b',
                'verbose_name_plural': '\u0417\u0430\u043a\u0430\u0437\u043d\u044b\u0435 \u043a\u0443\u043f\u043e\u043d\u044b',
            },
        ),
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100, verbose_name='\u0422\u0435\u043c\u0430')),
                ('text', models.TextField(null=True, verbose_name='\u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435', blank=True)),
                ('date', models.DateField(verbose_name='\u0414\u0430\u0442\u0430 \u0434\u043b\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438')),
                ('status', models.IntegerField(default=0, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', choices=[(0, '\u0412 \u043e\u0436\u0438\u0434\u0430\u043d\u0438\u0438'), (1, '\u0417\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0430')])),
            ],
            options={
                'ordering': ['-status', 'date'],
                'verbose_name': '\u041f\u0438\u0441\u044c\u043c\u043e',
                'verbose_name_plural': '\u041f\u0438\u0441\u044c\u043c\u0430',
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=64, null=True, verbose_name='\u0418\u043c\u044f', blank=True)),
                ('last_name', models.CharField(max_length=64, null=True, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f', blank=True)),
                ('phone', models.CharField(max_length=50, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d', blank=True)),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='Email')),
                ('status', models.IntegerField(default=1, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', choices=[(0, '\u041d\u0435 \u043f\u043e\u0434\u043f\u0438\u0441\u0430\u043d'), (1, '\u041f\u043e\u0434\u043f\u0438\u0441\u0430\u043d')])),
            ],
            options={
                'ordering': ['-status', 'email'],
                'verbose_name': '\u041f\u043e\u0434\u043f\u0438\u0441\u0447\u0438\u043a',
                'verbose_name_plural': '\u041f\u043e\u0434\u043f\u0438\u0441\u0447\u0438\u043a\u0438',
            },
        ),
        migrations.AddField(
            model_name='letter',
            name='recipients',
            field=models.ManyToManyField(to='distribution.Subscriber', verbose_name='\u041f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u0438'),
        ),
        migrations.AddField(
            model_name='couponsubscriber',
            name='subscriber',
            field=models.ForeignKey(to='distribution.Subscriber'),
        ),
    ]
