# -*- coding: utf-8

from django import forms
from django.forms.formsets import BaseFormSet
from models import Category, Item, ItemVideo, ImportTask, Order, OrderItem, CurrencySetting
from apps.account.models import ExtendedProfile
from apps.account.forms import SignupForm2
from django.forms.widgets import CheckboxSelectMultiple
from utils2.enum_choices import EnumChoices
from apps.website.models import Point
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['catalog']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ['order']


class CurrencySettingForm(forms.ModelForm):
    class Meta:
        model = CurrencySetting
        exclude = ('site',)


class PointForm(forms.ModelForm):
    class Meta:
        model = Point
        exclude = ['user', 'outlet_id']
        fields_required = ('city', 'street', 'address',)
        readonly = ('name_1c',)

    def __init__(self, *args, **kwargs):
        super(PointForm, self).__init__(*args, **kwargs)
        self.fields['lat'].widget = forms.HiddenInput()
        self.fields['lat'].label = ''
        self.fields['lon'].widget = forms.HiddenInput()
        self.fields['lon'].label = ''
        self.fields['name_1c'].widget.attrs['readonly'] = True


class CategoryForm(forms.ModelForm):
    class Meta(object):
        model = Category
        exclude = ['catalog', 'slug', 'active', 'parameters']

    def __init__(self, *args, **kwargs):
        catalog = kwargs.pop('catalog', None)
        exclude_id = kwargs.pop('exclude_id', None)
        cat_id = kwargs.pop('cat_id', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Category.objects.filter(catalog=catalog).exclude(id=exclude_id).reverse()
        if cat_id:
            # self.fields['parent'].queryset = Category.objects.filter(catalog=catalog).get(id=cat_id).get_ancestors()
            self.fields['parent'].queryset = Category.objects.filter(catalog=catalog)  # .get(id=cat_id)
        initial = u'<img width="50" class="thumbnail" src="%s">' % (self.instance.get_image_thumb50_url(),)
        clear_template = u'<label for="image-clear_id" class="checkbox"><input id="image-clear_id" type="checkbox" name="image-clear"> очистить</label>'
        self.fields['image'].widget.template_with_initial = initial + clear_template + '%(input_text)s: %(input)s'
        self.fields[
            'image'].widget.template_with_clear = u'%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'
        self.fields['parent'].label = u'Родитель'
        self.fields['name'].label = u'Наименование'


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = [
        'site', 'parameters', 'currency', 'image_count', 'video_count', 'priceRUAH', 'priceRUSD', 'priceOUSD', 'url',
        'hit_counter', 'point']

    def __init__(self, *args, **kwargs):
        catalog = kwargs.pop('catalog', None)
        category = kwargs.pop('category', None)
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(catalog=catalog).reverse()
        currency_setting = CurrencySetting.objects.filter(site=catalog.website)
        self.fields['price'].help_text = mark_safe(u'Укажите цену в %s или <a href="%s">измените валюту</a>' % (
            currency_setting[0].get_currency_display() if currency_setting else 'UAH',
            reverse('filter')
        )
                                                   )
        if category:
            self.fields['category'].initial = category


class ItemVideoForm(forms.ModelForm):
    class Meta:
        model = ItemVideo
        exclude = ['item']


class ParamsForm(forms.Form):
    name = forms.CharField(label=u'Параметр', max_length=50, required=False)
    value = forms.CharField(label=u'Значение', max_length=50, required=False)


class ImportTaskForm(forms.ModelForm):
    class Meta:
        model = ImportTask
        # fields = ('data', 'url', 'pid', 'format')
        fields = ('data', 'url', 'pid')

    def __init__(self, *args, **kwargs):
        website_property = kwargs.pop('website_property', None)
        super(ImportTaskForm, self).__init__(*args, **kwargs)

        # self.fields['format'].choices[0].widget.attrs['value'] = '1'
        # if website_property.imp_exp_exel==0:
        #     # self.fields['format'].widget.attrs['disabled'] = 'disabled'


class FilterForm(forms.Form):
    SALE = EnumChoices((
        (0, u'Все результаты', 'ALL'),
        (1, u'Не установлена', 'UNMARKED'),
        (2, u'Установлена', 'MARKED'),
    ))

    vendor = forms.ChoiceField(widget=forms.Select(), label=u'Бренд', required=False)
    wholesale = forms.ChoiceField(label=u'Оптовая продажа', choices=SALE)
    discount = forms.CharField(label=u'Скидка', required=False,
                               help_text=u'Число от 0 до 100, можно использовать знаки > и < перед ним')

    def __init__(self, *args, **kwargs):
        catalog = kwargs.pop('catalog', None)
        super(FilterForm, self).__init__(*args, **kwargs)
        item_vendors = Item.objects.filter(category__catalog=catalog).order_by('vendor').exclude(vendor=None).values_list('vendor', flat=True)
        self.fields['vendor'].choices = map(lambda x: ('%s' % x, '%s' % x), sorted(set(item_vendors)))

    def clean_wholesale(self):
        if FilterForm.SALE.MARKED == int(self.cleaned_data['wholesale']):
            self.cleaned_data['wholesale'] = True
        elif FilterForm.SALE.UNMARKED == int(self.cleaned_data['wholesale']):
            self.cleaned_data['wholesale'] = False
        else:
            self.cleaned_data['wholesale'] = ''
        return self.cleaned_data['wholesale']

    def clean_discount(self):
        if self.cleaned_data.get('discount'):
            try:
                s, i = (self.cleaned_data['discount'][0], int(self.cleaned_data['discount'][1:])) \
                    if self.cleaned_data['discount'][0] in '<>' else (None, int(self.cleaned_data['discount']))
            except ValueError:
                raise forms.ValidationError(u'Скидка должна быть числом от 0 до 100')
            if i > 100 or i < 0:
                raise forms.ValidationError(u'Скидка должна быть числом от 0 до 100')
            key = 'discount__lt' if s == '<' else 'discount__gt' if s == '>' else 'discount'
            self.cleaned_data[key] = i

    def clean(self):
        for k, v in self.cleaned_data.items():
            if v in ('', None):
                del self.cleaned_data[k]
        return self.cleaned_data


class ActionForm(forms.Form):
    SALE = EnumChoices((
        (0, u'Не применять', 'DONT_USE'),
        (1, u'Установить', 'MARK'),
        (2, u'Отменить', 'UNMARK'),
    ))
    discount = forms.IntegerField(label=u'Скидка, 0-100%', max_value=100, min_value=0, required=False)
    wholesale = forms.ChoiceField(label=u'Оптовая продажа', choices=SALE)

    def clean_wholesale(self):
        if ActionForm.SALE.MARK == int(self.cleaned_data['wholesale']):
            self.cleaned_data['wholesale'] = True
        elif ActionForm.SALE.UNMARK == int(self.cleaned_data['wholesale']):
            self.cleaned_data['wholesale'] = False
        else:
            self.cleaned_data['wholesale'] = ''
        return self.cleaned_data['wholesale']

    def clean(self):
        for k, v in self.cleaned_data.items():
            if v in ('', None):
                del self.cleaned_data[k]
        return self.cleaned_data


class ExprofileEditForm(forms.ModelForm):
    PAY_OPTION = (
        ('1', 'Оплата курьеру'),
        ('2', 'Наложенный платёж'),
        ('3', 'Visa, MasterCard'),
        ('4', 'Безналичная оплата с НДС'),
        ('5', 'Кредит')
    )

    TRANS_COMP = (
        ('1', 'По Украине'),
        ('2', 'По России'),
        ('3', 'По Белоруссии'),
        ('4', 'По СНГ'),
        ('5', 'Самовывоз')
    )

    class Meta(object):
        model = ExtendedProfile
        exclude = ['user', 'li_id', 'mr_id', 'meta', 'nds', 'wholesale_trade', 'credit_sale']
        widgets = {
            'store_address': forms.HiddenInput(),
            'store_name': forms.HiddenInput()

        }

    site_name = forms.CharField(
        label=u'Название магазина', required=False)
    phone_number = forms.CharField(
        label=u'Телефон для связи с администрацией', required=False)
    phone_call_center = forms.CharField(
        label=u'Телефон call-центра(для сайта)', required=False)
    payment_methods = forms.MultipleChoiceField(
        label=u'Способы оплаты', required=False,
        widget=CheckboxSelectMultiple, choices=PAY_OPTION)
    delivery = forms.MultipleChoiceField(
        label=u'Доставка', required=False, widget=CheckboxSelectMultiple,
        choices=TRANS_COMP)

    def clean(self):
        for k, v in self.cleaned_data.items():
            if v == '':
                self.cleaned_data[k] = None
        return self.cleaned_data
