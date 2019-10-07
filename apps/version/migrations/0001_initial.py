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
            name='Version',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(choices=[(0, '\u041f\u043e\u043a\u0443\u043f\u043a\u0430 \u0432 \u0440\u0430\u0441\u0441\u0440\u043e\u0447\u043a\u0443'), (1, '\u041e\u0431\u0440\u0430\u0442\u043d\u0430\u044f \u0441\u0432\u044f\u0437\u044c')])),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430')),
                ('user', models.ForeignKey(related_name='versions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0412\u0435\u0440\u0441\u0438\u044f',
                'verbose_name_plural': '\u0412\u0435\u0440\u0441\u0438\u0438',
            },
        ),
        migrations.AlterUniqueTogether(
            name='version',
            unique_together=set([('user', 'type')]),
        ),
    ]
