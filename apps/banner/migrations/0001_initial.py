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
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'banners')),
                ('active', models.BooleanField()),
                ('count', models.IntegerField()),
                ('redirect', models.URLField()),
                ('date_add', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('user', models.ForeignKey(related_name='banners', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='banner',
            unique_together=set([('user', 'image')]),
        ),
    ]
