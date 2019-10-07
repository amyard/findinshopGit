# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, verbose_name='\u0418\u043c\u044f')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('text', models.TextField(verbose_name='\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430')),
            ],
        ),
    ]
