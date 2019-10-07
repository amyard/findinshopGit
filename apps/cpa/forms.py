# -*- coding: utf-8 -*-

#Python imports
from datetime import timedelta

#Django imports
from django import forms
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.cache import cache

#Findinshop
from apps.cpa.models import CostSetting, OwnAndUserCategory
from apps.cpa.validators import MIN_COST_RATE
from apps.cpa.utils import float_to_python
from apps.section.models import Section
from apps.catalog.models import Category
from apps.website.models import Website


class CategoryCostForm(forms.ModelForm):

    class Meta:
        model = CostSetting
        fields = ('section', 'current_rate')

    def __init__(self, *args, **kwargs):
        super(CategoryCostForm, self).__init__(*args, **kwargs)
        self.fields['section'].queryset = Section.parents.all()
        self.fields['current_rate'].help_text = 'Минимальная стоимость %s грн.' % MIN_COST_RATE
        self.fields['current_rate'].to_python = float_to_python

    def clean(self):
        cleaned_data = super(CategoryCostForm, self).clean()
        section = cleaned_data.get('section')
        if section and self.user:
            #setting = get_object_or_404(CostSetting, user=self.user, section=section)
            setting, created = CostSetting.objects.get_or_create(user=self.user, section=section)

            if setting.current_rate == cleaned_data.get('current_rate'):
                raise forms.ValidationError(u'Такая ставка уже установлена.')

            if setting.changed is True:
                time_tree_hour_ago = timezone.now() - timedelta(hours=3)

                if time_tree_hour_ago < setting.date_change:
                    raise forms.ValidationError(u'Повторное изменение ставки на эту категорию возможно через 3 часа')

        return cleaned_data


class OwnAndUserCategoryForm(forms.ModelForm):

    class Meta:
        model = OwnAndUserCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OwnAndUserCategoryForm, self).__init__(*args, **kwargs)

        #if not cache.get('key_queryset_section_children_admin', False):
        #    queryset_section = Section.children.all().order_by('parent__name')
        #    cache.set('key_queryset_section_children_admin', queryset_section, 2*3600)#2 hours
        #else:
        #    queryset_section = cache.get('key_queryset_section_children_admin')

        #self.fields['our_section'].queryset = queryset_section


        self.fields['our_section'].queryset = Section.parents.all()

        if self.instance.pk:
            self.fields['categories'].queryset = Category.objects.filter(catalog=self.instance.site.catalog)
        else:
            self.fields['categories'].choices = Category.objects.none()

        self.fields['site'].queryset = Website.objects.order_by('subdomain')


class ReportClickForm(forms.Form):

    date_from = forms.DateField(
                    label=u'Начиная с даты',
                    #input_formats='%d.%m.%Y'
            )
    date_to = forms.DateField(
                    label=u'Заканчивая датой',
                    #input_formats='%d.%m.%Y'
            ) 
