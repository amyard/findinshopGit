# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importtask',
            name='validity',
            field=models.BooleanField(default=False, verbose_name='URL \u043f\u0440\u043e\u0432\u0435\u0440\u0435\u043d'),
        ),
    ]
