# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='\u0422\u0435\u043c\u0430')),
                ('submitted_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(null=True, verbose_name='\u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435', blank=True)),
                ('status', models.IntegerField(default=0, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', choices=[(0, '\u041e\u0442\u043a\u0440\u044b\u0442\u0430'), (1, '\u041e\u0431\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u0435\u0442\u0441\u044f'), (2, '\u0417\u0430\u043a\u0440\u044b\u0442\u0430')])),
                ('priority', models.IntegerField(default=0, verbose_name='\u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442', choices=[(0, '\u041d\u0438\u0437\u043a\u0438\u0439'), (1, '\u0421\u0440\u0435\u0434\u043d\u0438\u0439'), (2, '\u0412\u044b\u0441\u043e\u043a\u0438\u0439')])),
                ('assigned_to', models.ForeignKey(related_name='assigned', verbose_name='\u041d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u043e', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('submitter', models.ForeignKey(related_name='submitter', verbose_name='\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('status', 'priority', 'submitted_date', 'title'),
            },
        ),
    ]
