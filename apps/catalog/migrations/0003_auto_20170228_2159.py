# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20170227_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='gender',
            field=models.CharField(default=b'0', max_length=2, choices=[(b'0', '\u041d\u0435 \u0443\u043a\u0430\u0437\u0430\u043d'), (b'1', '\u041c\u0443\u0436\u0441\u043a\u043e\u0439'), (b'2', '\u0416\u0435\u043d\u0441\u043a\u0438\u0439')]),
        ),
    ]
