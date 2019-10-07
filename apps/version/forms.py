# -*- coding: utf-8 -*-
from django import forms

from models import Version


class VersionForm(forms.Form):

    class Meta:
        model = Version

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        versions = Version.objects.filter(user=self.user).values_list('type', flat=True)
        super(VersionForm, self).__init__(*args, **kwargs)
        for i, version in Version.TYPE:
            self.fields['%s' % i] = forms.BooleanField(label=version, required=False)
            # if i == 0:
            #     self.fields['%s' % i].widget.attrs['disabled'] = 'disabled'
            if i in versions:
                self.fields['%s' % i].initial = True

    def save(self, *args, **kwargs):
        for ver, val in self.cleaned_data.items():
            v, created = Version.objects.get_or_create(user=self.user, type=ver, defaults={'user': self.user, 'type': ver})
            if v and not val:
                v.delete()
