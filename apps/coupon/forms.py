# -*- coding: utf-8 -*-

import uuid
from datetime import datetime

#Django imports
from django import forms

#Apps imports
from apps.coupon.models import Coupon


class CouponForm(forms.ModelForm):

    class Meta:
        model = Coupon
        exclude = ('user', 'filters', 'items', 'count')

    def __init__(self, *args, **kwargs):
        super(CouponForm, self).__init__(*args, **kwargs)
        self.fields['code'].initial = uuid.uuid4().hex[:10]
        self.fields['date_start'].initial = datetime.now()


class GetCoupon(forms.Form):
    name = forms.CharField(label=u'Имя')
    email = forms.EmailField(label=u'Email')
    phone = forms.CharField(label=u'Телефон')
