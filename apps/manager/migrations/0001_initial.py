# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('url', models.URLField(null=True, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430', blank=True)),
                ('image', models.ImageField(upload_to=b'banners', verbose_name='\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0430')),
                ('active', models.BooleanField(default=True, verbose_name='\u041f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0442\u044c?')),
                ('sort', models.SmallIntegerField(default=0, verbose_name='\u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442 \u0432 \u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0435')),
            ],
            options={
                'ordering': ['-sort'],
                'verbose_name': '\u0411\u0430\u043d\u043d\u0435\u0440',
                'verbose_name_plural': '\u0411\u0430\u043d\u043d\u0435\u0440\u0430',
            },
        ),
    ]
