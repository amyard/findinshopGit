#-*- coding:utf-8 -*-
from datetime import datetime

from django.db import models
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
# from django.template.loader import get_template_from_string 
# get_template_from_string was removed in 1.8
from django.template import loader, engines

from django.template import RequestContext
from django.http import HttpRequest

class Message(models.Model):
    key = models.CharField(max_length=200, unique=True)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'Шаблон письма'
        verbose_name_plural = u'Шаблоны писем'

    def __unicode__(self):
        return self.key

    def __init__(self, *args, **kwargs):
        super(Message, self).__init__(*args, **kwargs)
        self._item = dict([(i.locale, i) for i in self.messageitem_set.all()])

    def send(self, recipients, sender=settings.DEFAULT_FROM_EMAIL, locale=settings.LANGUAGE_CODE, **context):
        if isinstance(recipients, (str, unicode)):
            recipients = [recipients,]
        try:
            mi = self.messageitem_set.get(locale=locale)
        except KeyError:
            raise Exception('Message with locale %s does not exist' % locale)

        # template_title = get_template_from_string(mi.title)
        # template_text = get_template_from_string(mi.body_text)
        # template_html = get_template_from_string(mi.body_html)
        try:
            template_title = loader.get_template_from_string(mi.title)
            template_text = loader.get_template_from_string(mi.body_text)
            template_html = loader.get_template_from_string(mi.body_html)
        except AttributeError: # get_template_from_string was removed in 1.8
            template_title = engines['django'].from_string(mi.title)
            template_text = engines['django'].from_string(mi.body_text)
            template_html = engines['django'].from_string(mi.body_html)

        title = template_title.render(RequestContext(HttpRequest(), context))
        message_text = template_text.render(RequestContext(HttpRequest(), context))
        message_html = template_html.render(RequestContext(HttpRequest(), context))

        msg = EmailMultiAlternatives(title, message_text, sender, recipients)
        msg.attach_alternative(message_html, 'text/html')
        msg.send()

class MessageItem(models.Model):
    message = models.ForeignKey(Message)
    title = models.CharField(max_length=255)
    body_text = models.TextField()
    body_html = models.TextField()
    locale = models.CharField(max_length=5, default=settings.LANGUAGE_CODE)

    def __unicode__(self):
        return self.message.key

