# -*- coding: utf-8
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .html2text import html2text

def message_send(subject, to_email, template, context=None, from_addr=None):
    """
    Send message
    """
    message = render_to_string(template, context)
    email = EmailMultiAlternatives(
        subject,
        html2text(message),
        from_addr,
        to_email
    )
    email.attach_alternative(message, 'text/html')
    email.send()