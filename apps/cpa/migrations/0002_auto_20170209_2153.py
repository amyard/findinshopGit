# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('section', '0001_initial'),
        ('cpa', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0001_initial'),
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='section',
            field=models.ForeignKey(blank=True, to='section.Section', null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='refreshcosttask',
            name='setting',
            field=models.ForeignKey(to='cpa.CostSetting'),
        ),
        migrations.AddField(
            model_name='ownandusercategory',
            name='categories',
            field=models.ManyToManyField(to='catalog.Category', verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u0441\u043a\u0438\u0435 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438'),
        ),
        migrations.AddField(
            model_name='ownandusercategory',
            name='our_section',
            field=models.ForeignKey(verbose_name='\u041d\u0430\u0448 \u0440\u0430\u0437\u0434\u0435\u043b', to='section.Section'),
        ),
        migrations.AddField(
            model_name='ownandusercategory',
            name='site',
            field=models.ForeignKey(verbose_name='Web \u0441\u0430\u0439\u0442', to='website.Website'),
        ),
        migrations.AddField(
            model_name='costsetting',
            name='section',
            field=models.ForeignKey(to='section.Section'),
        ),
        migrations.AddField(
            model_name='costsetting',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
