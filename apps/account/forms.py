# -*- coding: utf-8

from django import forms
from django.contrib.auth.models import User, Permission, Group
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from models import Profile, ExtendedProfile
from apps.website.models import Website, WebsiteProperty
from utils2.email import message_send
# from apps.account.models import Profile
from django.forms.widgets import CheckboxSelectMultiple
import datetime
from django.core.exceptions import ObjectDoesNotExist
from apps.account.tasks import manager_notify_task


class SignupForm(forms.ModelForm):

    WEB_PR = WebsiteProperty.objects.filter(online_shop=0).values_list('id', 'name')

    # username = forms.RegexField(label="Логин", max_length=30, regex=r'^[\w.@+-]+$',
                                # help_text="Введите 30 символов или менее. Используйте только латинские буквы в нижнем регистре, цифры и знаки из набора @/./+/-/_",
                                # error_messages={'invalid': "Это поле должно содержать только латинские буквы в нижнем регистре, цифры и знаки из набора @/./+/-/_"})
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False), label=u'Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False), label=u'Пароль повторно')
    subdomain = forms.CharField(label=u'Внутренний адрес магазина', help_text="Пока не настроен домен магазин будет доступен по адресу вида myshop.%s" % settings.BASE_DOMAIN, required=True)
    domain = forms.CharField(label=u'Доменное имя', help_text="Для магазина можно будет позднее настроить собственное доменное имя вида myshop.net", required=False)
    phone = forms.CharField(label=u'Телефон для связи с администрацией')
    phone_call_center = forms.CharField(label=u'Телефон call-центра(для сайта)')
    # location_site = forms.IntegerField(label=u'Локализация сайта', widget=forms.Select(choices=Website.LOCATION))

    # have_yml = forms.IntegerField(label=u'Наличие прайс-листа в формате YML', widget=forms.Select(choices=Website.HAVE_YML))

    class Meta:
        model = User
        fields = ['email', 'first_name']

    def __init__(self, *args, **kwargs):
        online_shop = kwargs.pop('online_shop', None)
        super(SignupForm, self).__init__(*args, **kwargs)
        if online_shop:
            self.fields['wholesale_trade'] = forms.BooleanField(label=u'Оптовая продажа', required=False)
        self.fields['email'].required = True
        # self.fields['web_property'] = forms.IntegerField(label=u'Тарифный план', widget=forms.Select(choices=SignupForm.WEB_PR))

    def clean_email(self):
        try:
            if Profile.objects.filter(email__iexact=self.cleaned_data['email'].lower()).exists():
                raise forms.ValidationError(u'Email уже зарегестрирован')
        except Profile.DoesNotExist:
            pass
        return self.cleaned_data['email'].lower()

    def clean_subdomain(self):
        if 'subdomain' in self.cleaned_data:
            try:
                if Website.objects.filter(subdomain__iexact=self.cleaned_data['subdomain'].lower()).count():
                    raise forms.ValidationError(u'Такой адрес уже существует')
            except Website.DoesNotExist:
                pass
            return self.cleaned_data['subdomain'].lower()
        else:
            return self.cleaned_data

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(u'Вы должны указать два раза один и тот же пароль')
        return self.cleaned_data

    def save(self, *args, **kwargs):
        self.instance.username = self.cleaned_data['email'].lower()
        instance = super(SignupForm, self).save(*args, **kwargs)
        instance.set_password(self.cleaned_data['password1'])
        instance.is_active = False
        try:
            group = Group.objects.get(name='Have website')
        except ObjectDoesNotExist:
            group = Group(name='Have website')
            group.save()
        instance.groups.add(group)
        instance.save()

        profile = Profile(user=instance)
        profile.phone_number = self.cleaned_data['phone']
        profile.email = self.cleaned_data['email'].lower()
        profile.save()
        website = Website(user=instance)
        website.domain = self.cleaned_data['domain']
        if self.cleaned_data.get('subdomain'):
            website.subdomain = self.cleaned_data['subdomain']
        website.phone_call_center = self.cleaned_data['phone_call_center']
        website.web_property_id = 1  # self.cleaned_data['web_property']
        website.location_site = 0
        website.save()
        # website.location_site = self.cleaned_data['location_site']
        # website.have_yml = self.cleaned_data['have_yml']
        return instance


class SignupForm2(forms.ModelForm):

    WEB_PR = WebsiteProperty.objects.filter(online_shop=1).values_list('id', 'name')

    PAY_OPTION = (('1', 'Оплата курьеру'),
                  ('2', 'Наложенный платёж'),
                  ('3', 'Visa, MasterCard'),
                  ('4', 'WebMoney'),
                  #('5', 'Оплата курьеру'),
                  ('6', 'Безналичная оплата с НДС'),
                  ('7', 'Кредит'))

    DAYS_WEEK = (('1', 'Пн.'),
                 ('2', 'Вт.'),
                 ('3', 'Ср.'),
                 ('4', 'Чт.'),
                 ('5', 'Пт.'),
                 ('6', 'Сб.'),
                 ('7', 'Вс.'))

    TRANS_COMP = (('1', 'По Украине'),
                  ('2', 'По России'),
                  ('3', 'По Белоруссии'),
                  ('4', 'По СНГ'),
                  ('5', 'Курьером'),
                  ('6', 'Почтой'),
                  ('7', 'Самовывоз'))


    #username = forms.RegexField(label="Логин", max_length=30, regex=r'^[\w.@+-]+$',
    #                            help_text="Введите не менее 4х символов. Используйте только латинские буквы в нижнем регистре, цифры и знаки из набора @/./+/-/_",
    #                            error_messages={'invalid': "Это поле должно содержать только латинские буквы в нижнем регистре, цифры и знаки из набора @/./+/-/_"})
    phone = forms.CharField(label=u'Телефон для связи с администрацией')
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False), label=u'Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False), label=u'Пароль повторно')
    # web_property = forms.IntegerField(label=u'Тарифный план', widget=forms.Select(choices=WEB_PR))
    # subdomain = forms.CharField(label=u'Внутренний адрес магазина', help_text="Пока не настроен домен магазин будет доступен по адресу вида myshop.%s" % settings.BASE_DOMAIN, required=True)

    phone_call_center = forms.CharField(label=u'Телефон call-центра(для сайта)')
    # phone_call_center = forms.CharField(label=u'Телефон call-центра')
    # have_yml = forms.IntegerField(label=u'Наличие прайс-листа в формате YML', widget=forms.Select(choices=Website.HAVE_YML))

    # store_name = forms.CharField(label=u'Название магазина', max_length=50)
    # city = forms.CharField(label=u'Город', max_length=50)
    # contact_name = forms.CharField(label=u'Ф.И.О. контактного лица', max_length=50)
    label = """
    <a href="http://help.yandex.ru/partnermarket/?id=1111425&ncrnd=6006" target="_blank">YML</a>
    """
    link_XML = forms.URLField(label=u'Ссылка на XML файл (в формате %s)' % label)
    # credit_sale = forms.IntegerField(widget=forms.Select(choices=ExtendedProfile.SEL), label=u'Прайс-лист YML')
    # credit_sale = forms.BooleanField(label=u'Продажа в кредит',required=False)
    # payment_methods = forms.MultipleChoiceField(label=u'Способы оплаты', required=False, widget=CheckboxSelectMultiple, choices=PAY_OPTION)

    # logo = forms.ImageField(label=u'Логотип компании')
    # nds = forms.BooleanField(label=u'НДС',required=False)
    # wholesale_trade = forms.BooleanField(label=u'Оптовая продажа',required=False)
    # mode = forms.MultipleChoiceField(label=u'Режим работы', required=False, widget=CheckboxSelectMultiple, choices=DAYS_WEEK)
    # time_of = forms.TimeField(label=u'Время работы с', widget=forms.TimeInput(format='%H:%M'))
    # time_to = forms.TimeField(label=u'Время работы по', widget=forms.TimeInput(format='%H:%M'))
    # delivery = forms.MultipleChoiceField(label=u'Доставка по Украине', required=False, widget=CheckboxSelectMultiple, choices=TRANS_COMP)
    # store_address = forms.CharField(label=u'Адрес магазина', max_length=100)

    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(SignupForm2, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_email(self):
        try:
            if User.objects.filter(email__iexact=self.cleaned_data['email'].lower()).count():
                raise forms.ValidationError(u'Это email уже зарегестрирован.')
        except User.DoesNotExist:
            pass
        return self.cleaned_data['email'].lower()

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(u'Вы должны указать два раза один и тот же пароль')
        return self.cleaned_data

    def save(self, *args, **kwargs):
        self.instance.username = self.cleaned_data['email'].lower()
        instance = super(SignupForm2, self).save(*args, **kwargs)
        instance.set_password(self.cleaned_data['password1'])
        instance.is_active = False
        instance.save()

        instance.profile.phone_number = self.cleaned_data['phone']
        instance.profile.save()

        # instance.website.logo = self.cleaned_data['logo']
        instance.website.phone_call_center = self.cleaned_data['phone_call_center']
        # instance.website.name = self.cleaned_data['store_name']
        instance.website.location_site = 1
        instance.website.web_property_id = 1  # self.cleaned_data['web_property']
        instance.website.save()

        instance.eprofile.link_XML = self.cleaned_data['link_XML']
        # instance.eprofile.store_name = self.cleaned_data['store_name']
        # instance.eprofile.contact_name = self.cleaned_data['contact_name']
        # instance.eprofile.credit_sale = self.cleaned_data['credit_sale']
        # instance.eprofile.payment_methods = self.cleaned_data['payment_methods']
        # instance.eprofile.nds = self.cleaned_data['nds']
        # instance.eprofile.wholesale_trade = self.cleaned_data['wholesale_trade']
        # instance.eprofile.mode = self.cleaned_data['mode']
        # instance.eprofile.delivery = self.cleaned_data['delivery']
        # instance.eprofile.store_address = self.cleaned_data['store_address']
        # instance.eprofile.city = self.cleaned_data['city']
        # instance.eprofile.time_of = self.cleaned_data['time_of']
        # instance.eprofile.time_to = self.cleaned_data['time_to']
        instance.eprofile.save()
        return instance


class SignupForm3(SignupForm):

    def __init__(self, *args, **kwargs):
        super(SignupForm3, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.username = self.cleaned_data['email'].lower()
        instance = super(SignupForm, self).save(*args, **kwargs)
        instance.set_password(self.cleaned_data['password1'])
        instance.is_active = False
        instance.save()
        instance.profile.phone_number = self.cleaned_data['phone']
        instance.profile.save()
        instance.website.domain = self.cleaned_data['domain']
        if self.cleaned_data.get('subdomain'):
            instance.website.subdomain = self.cleaned_data['subdomain']
        instance.website.phone_call_center = self.cleaned_data['phone_call_center']
        instance.website.web_property_id = 3
        instance.website.location_site = 0
        instance.website.save()
        return instance


class ProfileEditForm(forms.ModelForm):

    first_name = forms.CharField(label=u'Имя', required=False)
    last_name = forms.CharField(label=u'Фамилия', required=False)

    class Meta:
        model = Profile
        exclude = ['user', 'balance', 'userpic']
        # fields = ['first_name', 'last_name', 'phone_number', 'userpic']

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        initial = u'<img width="50" class="thumbnail" src="%s">' % (self.instance.get_userpic_thumb50_url(), )
        clear_template = u'<label for="userpic-clear_id" class="checkbox"><input id="userpic-clear_id" type="checkbox" name="userpic-clear"> очистить</label>'
        #self.fields['userpic'].widget.template_with_initial = initial + clear_template + '%(input_text)s: %(input)s'
        #self.fields['userpic'].widget.template_with_clear = u'%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'
        self.fields['firmname'].label = u'Название фирмы (для налоговых накладных)'

    def save(self, *args, **kwargs):
        inst = super(ProfileEditForm, self).save(*args, **kwargs)
        inst.user.first_name = self.cleaned_data['first_name']
        inst.user.last_name = self.cleaned_data['last_name']
        inst.user.save()
        return inst


class SignupTemplateMarketForm(forms.ModelForm):

    password1 = forms.CharField(
        widget=forms.PasswordInput(render_value=False),
        label=_(u'Пароль'))
    password2 = forms.CharField(
        widget=forms.PasswordInput(render_value=False),
        label=_(u'Пароль повторно'))
    phone = forms.CharField(
        label=_(u'Телефон для связи с администрацией'), required=False)

    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(SignupTemplateMarketForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control input-lg'
        self.fields['email'].required = True

    # def clean_email(self):
    #     value = self.cleaned_data['email'].lower()
    #     if User.objects.filter(email=value).exists():
    #         raise forms.ValidationError(_(u'Email уже зарегестрирован'))
    #     return value
    def clean_email(self):
        try:
            if Profile.objects.filter(email__iexact=self.cleaned_data['email'].lower()).exists():
                raise forms.ValidationError(u'Email уже зарегестрирован')
        except Profile.DoesNotExist:
            pass
        return self.cleaned_data['email'].lower()

    # def clean_phone(self):
    #     value = self.cleaned_data['phone']
    #     if User.objects.filter(email=value).exists():
    #         raise forms.ValidationError(_(u'Email уже зарегестрирован'))
    #     return value

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    _(u'Вы должны указать два раза один и тот же пароль')
                )
        return password2

    def get_market_type(self):
        """
        Return information about market (Online or Offline)
        :return:
        """
        pass

    def get_program_type(self):
        """
        Return information about market (Online or Offline)
        :return:
        """
        pass

    def manager_notify(self):
        context = self.cleaned_data
        context['is_offline_market'] = self.get_market_type()
        context['program'] = self.get_program_type()
        context['market_type'] = Website.TYPE.get_name(self.get_market_type())
        manager_notify_task.delay(u"Новый магазин зарегистрирован",
            [settings.MANAGER_MAIL, ], 'emails/signup_market.html', context)
        # message_send(
        #     u"Новый магазин зарегистрирован",
        #     [settings.MANAGER_MAIL,],
        #     'emails/signup_market.html',
        #     context
        # )

    def save(self, *args, **kwargs):
        # TODO use old struct change in future
        self.instance.username = self.cleaned_data['email']
        user = super(SignupTemplateMarketForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        user.save()

        # Update profile
        profile = Profile()
        profile.user = user
        profile.phone_number = self.cleaned_data['phone']
        profile.email = self.cleaned_data['email'].lower()
        profile.save()

        # Update website
        website = Website()
        website.user = user
        website.subdomain = user.username.lower()
        website.type = self.get_market_type()
        # WebsiteProperty.pk == 1
        website.web_property_id = 1
        website.location_site = Website.LOCATION.Yes
        website.save()
        try:
            self.manager_notify()
        except Exception:
            print 'Fail to notify manager, after registration new magazine'
        return user


class SignupOnlineMarketForm(SignupTemplateMarketForm):
    link_XML = forms.URLField(
        label=_(u'Ссылка на XML файл'))

    def get_market_type(self):
        return Website.TYPE.ONLINE


class SignupOfflineMarketForm(SignupTemplateMarketForm):
    CONTROL_PROGRAM = (
        ('1', u'1с Управление Торговле 8.2'),
        ('2', u'1с Управление Торговым предприятием 8.2'),
        ('3', u'1с Управление Торговле 8.3'),
        ('4', u'1с Управление Торговым предприятием 8.3'),
        ('5', u'другая'))

    control_program = forms.ChoiceField(
        label=u'Управленческая программя',
        required=True,
        choices=CONTROL_PROGRAM)

    def get_market_type(self):
        return Website.TYPE.OFFLINE

    def get_program_type(self):
        return dict(self.CONTROL_PROGRAM).get(
            self.cleaned_data.get('control_program')
        )
