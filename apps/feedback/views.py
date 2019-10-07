# -*- coding: utf-8 -*-
from mailshelf import messages

from django.core.mail import mail_managers

from utils2.decorators import render_to
from apps.website.models import WebsiteProperty
from .forms import SupportForm


#@render_to('themes/findinshop/support.html')
@render_to('themes/findinshop/red/support.html')
def support(request):
    status = None
    form = SupportForm(request.POST or None)
    if request.method == 'POST' and form.is_valid() and form.cleaned_data:
        try:
            mail_managers(u'Вопрос с сайта', u'Вопрос от: %s, Почта для ответа: %s, Вопрос: %s' % (
                                                                                    form.cleaned_data['name'],
                                                                                    form.cleaned_data['email'],
                                                                                    form.cleaned_data['question']
                                                                            )
                                                            )
        #messages.send(email,
        #                            **{'name': request.POST.get('name'),
        #                               'email': request.POST.get('email'),
        #                               'question': request.POST.get('question')})
            status = 'ok'
        except Exception:
            status = 'error'
    return {'status': status, 'form': form}


@render_to('connect_shop.html')
def connect_shop(request):
    email = 'tolstoyant@gmail.com'
    status = None
    if request.method == 'POST':
        try:
            messages.CONNECTION_STORE.send(email,
                                           **{'store_name': request.POST.get('store_name'),
                                           'contact name': request.POST.get('contact name'),

                                           'login': request.POST.get('login'),
                                           'password': request.POST.get('password'),
                                           'password2': request.POST.get('password2'),
                                           'logo': request.POST.get('logo'),
                                           'id_web_property': WebsiteProperty.objects.get(id=request.POST.get('web_property')).name,

                                           'phone': request.POST.get('phone'),
                                           'email': request.POST.get('email'),
                                           'link_XML': request.POST.get('link_XML')})
            status = '1'
        except Exception:
            status = '0'
    return {'status': status}


@render_to('connect_shop.html')
def connect_shop_send(status):
    return {'status': status}
