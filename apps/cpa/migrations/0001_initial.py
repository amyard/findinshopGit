# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.cpa.validators


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count_item', models.IntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0442\u043e\u0432\u0430\u0440\u043e\u0432 \u0432 \u0440\u0430\u0437\u0434\u0435\u043b\u0435')),
                ('base_cost', models.FloatField(default=0, verbose_name='\u0411\u0430\u0437\u043e\u0432\u0430\u044f \u0441\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c \u043a\u043b\u0438\u043a\u0430')),
                ('current_rate', models.FloatField(default=0, verbose_name='\u0422\u0435\u043a\u0443\u0449\u0430\u044f \u0441\u0442\u0430\u0432\u043a\u0430', validators=[apps.cpa.validators.min_cost_rate])),
                ('total_cost', models.FloatField(default=0, verbose_name='\u041e\u0431\u0449\u0430\u044f \u0441\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c \u043a\u043b\u0438\u043a\u0430')),
                ('date_change', models.DateTimeField(auto_now=True)),
                ('changed', models.BooleanField(default=False, verbose_name='\u041c\u0435\u043d\u044f\u043b\u0430\u0441\u044c \u0441\u0442\u0430\u0432\u043a\u0430?')),
            ],
        ),
        migrations.CreateModel(
            name='OwnAndUserCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'ordering': ('site',),
                'verbose_name': '\u0421\u0432\u044f\u0437\u044c \u0441\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0445 \u0438 \u044e\u0437\u0435\u0440\u0441\u043a\u0438\u0445 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0439',
                'verbose_name_plural': '\u0421\u0432\u044f\u0437\u0438 \u0441\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0445 \u0438 \u044e\u0437\u0435\u0440\u0441\u043a\u0438\u0445 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0439',
            },
        ),
        migrations.CreateModel(
            name='RefreshCostTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_count', models.IntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u0435\u0440\u0435\u043e\u0446\u0435\u043d\u0435\u043d\u043d\u044b\u0445 \u0442\u043e\u0432\u0430\u0440\u043e\u0432')),
                ('status', models.IntegerField(default=0, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441 \u0437\u0430\u0434\u0430\u043d\u0438\u044f', choices=[(0, '\u041f\u0440\u0438\u043d\u044f\u0442'), (1, '\u041e\u0431\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u0435\u0442\u0441\u044f'), (2, '\u0412\u044b\u043f\u043e\u043b\u043d\u0435\u043d'), (3, '\u041e\u0448\u0438\u0431\u043a\u0430 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f')])),
                ('start', models.DateTimeField(null=True, verbose_name='\u041d\u0430\u0447\u0430\u043b\u043e \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f', blank=True)),
                ('complete', models.DateTimeField(null=True, verbose_name='\u041a\u043e\u043d\u0435\u0446 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f', blank=True)),
                ('error', models.TextField(null=True, verbose_name='\u041a\u043e\u0434 \u043e\u0448\u0438\u0431\u043a\u0438', blank=True)),
            ],
            options={
                'verbose_name': '\u0417\u0430\u0434\u0430\u043d\u0438\u0435 \u043f\u0435\u0440\u0435\u043e\u0446\u0435\u043d\u043a\u0438 \u0440\u0430\u0437\u0434\u0435\u043b\u0430',
                'verbose_name_plural': '\u0417\u0430\u0434\u0430\u043d\u0438\u044f \u043f\u0435\u0440\u0435\u043e\u0446\u0435\u043d\u043a\u0438 \u0440\u0430\u0437\u0434\u0435\u043b\u0430',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_name', models.CharField(max_length=255, verbose_name='\u0422\u043e\u0432\u0430\u0440')),
                ('cost', models.FloatField(verbose_name='\u0421\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c \u043a\u043b\u0438\u043a\u0430')),
                ('ip', models.CharField(max_length=20, null=True, verbose_name='IP \u0430\u0434\u0440\u0435\u0441', blank=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, to='catalog.Category', null=True)),
            ],
            options={
                'verbose_name': '\u041e\u0442\u0447\u0435\u0442 \u043e \u043a\u043b\u0438\u043a\u0430\u0445',
                'verbose_name_plural': '\u041e\u0442\u0447\u0435\u0442\u044b \u043e \u043a\u043b\u0438\u043a\u0430\u0445',
            },
        ),
    ]
