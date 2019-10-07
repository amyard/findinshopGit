# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(help_text='! \u041c\u043e\u0436\u0435\u0442\u0435 \u0443\u043a\u0430\u0437\u0430\u0442\u044c \u0441\u0432\u043e\u0439 \u043a\u043e\u0434', max_length=255, verbose_name='\u041a\u043e\u0434 \u043a\u0443\u043f\u043e\u043d\u0430')),
                ('size', models.PositiveSmallIntegerField(verbose_name='\u0420\u0430\u0437\u043c\u0435\u0440 \u0441\u043a\u0438\u0434\u043a\u0438')),
                ('types', models.CharField(default=b'P', max_length=1, verbose_name=b'\xd0\xa2\xd0\xb8\xd0\xbf \xd1\x81\xd0\xba\xd0\xb8\xd0\xb4\xd0\xba\xd0\xb8', choices=[(b'P', b'\xd0\x9f\xd1\x80\xd0\xbe\xd1\x86\xd0\xb5\xd0\xbd\xd1\x82\xd0\xbd\xd0\xb0\xd1\x8f'), (b'F', b'\xd0\xa4\xd0\xb8\xd0\xba\xd1\x81\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xbd\xd0\xb0\xd1\x8f')])),
                ('date_start', models.DateTimeField(help_text='\u0424\u043e\u0440\u043c\u0430\u0442: \u0447\u0438\u0441\u043b\u043e.\u043c\u0435\u0441\u044f\u0446.\u0433\u043e\u0434 \u0447\u0430\u0441\u044b:\u043c\u0438\u043d\u0443\u0442\u044b:\u0441\u0435\u043a\u0443\u043d\u0434\u044b. \u041f\u043e \u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e \u0441 \u043c\u043e\u043c\u0435\u043d\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', verbose_name='\u041a\u0443\u043f\u043e\u043d \u0434\u0435\u0439\u0441\u0442\u0432\u0443\u0435\u0442 \u0441')),
                ('date_end', models.DateTimeField(help_text='\u0424\u043e\u0440\u043c\u0430\u0442: \u0447\u0438\u0441\u043b\u043e.\u043c\u0435\u0441\u044f\u0446.\u0433\u043e\u0434 \u0447\u0430\u0441\u044b:\u043c\u0438\u043d\u0443\u0442\u044b:\u0441\u0435\u043a\u0443\u043d\u0434\u044b.', verbose_name='\u041a\u0443\u043f\u043e\u043d \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0442\u0435\u043b\u0435\u043d \u0434\u043e')),
                ('count', models.PositiveSmallIntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u0439')),
                ('filters', models.CharField(max_length=255, null=True, blank=True)),
                ('deleted', models.BooleanField(default=False, verbose_name=b'\xd0\xa3\xd0\xb4\xd0\xb0\xd0\xbb\xd0\xb5\xd0\xbd?')),
                ('items', models.ManyToManyField(to='catalog.Item', verbose_name='\u0422\u043e\u0432\u0430\u0440\u044b')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u041a\u0443\u043f\u043e\u043d',
                'verbose_name_plural': '\u041a\u0443\u043f\u043e\u043d\u044b',
            },
        ),
        migrations.AlterUniqueTogether(
            name='coupon',
            unique_together=set([('user', 'code')]),
        ),
    ]
