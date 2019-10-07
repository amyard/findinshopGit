# -*- coding: utf-8

from django.http import HttpResponse
from django.conf import settings
from apps.catalog.models import Order
import md5
from hashlib import sha1
import logging as log



def data_bank(request):
    pb_key = settings.P24_SECRET
    data = request.POST
    # data = "payment=amt=1&ccy=UAH&details=назначение&ext_details=назначение&pay_way=privat24&order=123&merchant=123&state=e&date=дата&ref=референс&sender_phone=телефон&signature=сигнатура"
    order = request.POST.get('order')
    # order=19031338
    rab_order = Order.objects.get(number=order)
    sign = "%s.%s" % (request.POST.get('payment'), pb_key)
    s1 = md5.new(sign)
    s1_str = str(s1)
    s2 = sha1(s1_str)

    if s2 == request.POST.get('signature'):
        log.info('IPN received %s' % request.POST.get('order'))
        status = "Успешно"
    else :
        log.info('IPN received %s' % request.POST.get('order'))
        status = "Несоответствие сигнатуры"
    # if pb_key:
    #     print "***************************************************** ", s2
    #     return HttpResponse('<h1>Page was found</h1>'+str(s2)+
    #                         # data.__getattribute__(data,details)+
    #     # '*****'+s1+'<br/>'+s2+
    #                         '')
    # else:
    #     print "-------------------------------------------------------------"
    #     return HttpResponse('<h1>Page not found</h1>')

    return HttpResponse(status)