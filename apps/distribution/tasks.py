# -*- coding: utf-8 -*-
from django.core.mail import EmailMultiAlternatives
from datetime import date

from celery.task import periodic_task, task
from celery.schedules import crontab

from models import Letter


@task(name='send_distribution', ignore_result=True, rate_limit='4/m')
def send_distribution(data, html):
    msg = EmailMultiAlternatives(*data)
    msg.attach_alternative(html, "text/html")
    msg.send()


@periodic_task(name='start_sending', ignore_result=True, run_every=crontab(minute=0, hour=10))
def start_sending():
    letters = Letter.objects.select_related().filter(status=Letter.STATUSES.PENDING, date=date.today())
    if letters:
        for letter in letters:
            for recipient in letter.recipients.all():
                html = "<html><body>%s</body></html>" % letter.text
                m = (letter.title, letter.text, 'info@on-s.net', [recipient.email])
                send_distribution.delay(m, html)
                letter.status = Letter.STATUSES.DONE
                letter.save()
