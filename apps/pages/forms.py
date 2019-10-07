# -*- coding: utf-8

from django import forms

from models import Page


class PageForm(forms.ModelForm):
    class Meta(object):
        model = Page
        exclude = ('website', 'page_type', 'slug', 'visibility')

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        if self.instance.page_type == 0:
            self.fields['title'].required = False
            self.fields['title'].widget.attrs['disabled'] = 'disabled'

    def clean_title(self):
        if self.instance.page_type == 0:
            return self.instance.title
        else:
            return self.cleaned_data['title']
