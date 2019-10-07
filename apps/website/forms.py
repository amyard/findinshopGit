# -*- coding: utf-8

import re
from django import forms
from django.forms import TextInput, Select

from models import Website, UserSpace, WebsiteProperty
# from apps.catalog.models import Item


class SiteEditForm(forms.ModelForm):
    class Meta(object):
        model = Website
        exclude = ('user', 'li_id', 'mr_id', 'meta', 'have_yml', 'location_site')
        widgets = {
            'subdomain': TextInput(attrs={'disabled': 'disabled'}),
            'web_property': Select(attrs={'disabled': 'disabled'}),

        }

    #rate = forms.FloatField(label=U'Курс валюты', required=False)

    def __init__(self, *args, **kwargs):
        website_property = kwargs.pop('website_property', None)

        super(SiteEditForm, self).__init__(*args, **kwargs)

        if hasattr(website_property, 'domain'):
            if website_property.domain==0:
                self.fields['domain'].widget.attrs['disabled'] = 'disabled'

        if hasattr(website_property, 'template_selection'):
            if website_property.template_selection==0:
                self.fields['skin'].widget.attrs['disabled'] = 'disabled'

        if hasattr(website_property, 'google_analistics'):
            if website_property.google_analistics==0:
                self.fields['ga_id'].widget.attrs['disabled'] = 'disabled'

        if hasattr(website_property, 'yandex_metrika'):
            if website_property.yandex_metrika==0:
                self.fields['ym_id'].widget.attrs['disabled'] = 'disabled'

        #self.fields['location_site'].widget.attrs['disabled'] = 'disabled'
        self.fields['subdomain'].required = False
        self.fields['web_property'].required = False
        initial = u'<img width="50" class="thumbnail" src="%s">' % (self.instance.get_logo_thumb50_url(), )
        clear_template = u'<label for="logo-clear_id" class="checkbox"><input id="logo-clear_id" type="checkbox" name="logo-clear"> очистить</label>'
        self.fields['logo'].widget.template_with_initial = initial + clear_template + '%(input_text)s: %(input)s'
        self.fields['logo'].widget.template_with_clear = u'%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'
        # self.fields['skin'].choices = [list(Website.SKINS)[0]]

    def clean_subdomain(self):
        return self.instance.subdomain

    def clean_web_property(self):
        return self.instance.web_property

    def clean_domain(self):
        regex = re.compile(
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?))'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if self.cleaned_data.get('domain') and not regex.search(self.cleaned_data.get('domain')):
            raise forms.ValidationError(u'Ошибка в формате домена!')
        else:
            return self.cleaned_data['domain']

    def clean(self):
        for k, v in self.cleaned_data.items():
            if v == '':
                self.cleaned_data[k] = None
        return self.cleaned_data


class UserSpaceForm(forms.ModelForm):
    class Meta:
        model = UserSpace
        exclude = ('key', 'website', 'content')


class FilterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category', None)
        super(FilterForm, self).__init__(*args, **kwargs)
        if self.category.parameters:
            for k in self.category.parameters.keys():
                self.fields['%s' % k] = forms.CharField(label=k, required=False)
                self.fields['%s' % k].widget.attrs['class'] = 'input-small'

    def clean(self):
        for k, v in self.cleaned_data.items():
            if not v:
                del self.cleaned_data[k]
        return self.cleaned_data
