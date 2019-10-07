#-*- coding:utf-8 -*-
from django import forms


class SubscribeForm(forms.Form):
    name = forms.CharField(max_length=80, label=u'Имя')
    email = forms.EmailField(label=u'Email')
