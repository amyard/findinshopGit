# -*- coding: utf-8

from django import forms

from models import Ticket


class TicketForm(forms.ModelForm):
    class Meta(object):
        model = Ticket
        exclude = ('assigned_to', 'submitter', 'status')
