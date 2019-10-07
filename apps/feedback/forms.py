#-*- coding:utf-8 -*-
from django import forms

from models import Message


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['name', 'email', 'text']

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs = {'style': 'width:400px;height:100px;'}


class SupportForm(forms.Form):
    name = forms.CharField(max_length=80, label=u'Имя')
    # phone = forms.CharField(label=u'Номер телефона')
    email = forms.EmailField(label=u'Email')
    question = forms.CharField(widget=forms.Textarea, label=u'Вопрос/комментарий')

