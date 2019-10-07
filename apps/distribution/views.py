# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from models import Subscriber

from utils.decorators import render_to

from forms import SubscribeForm


#@render_to('themes/findinshop/subscribe.html')
@render_to('themes/findinshop/red/subscribe.html')
def add_subscriber(request):
    status = None
    form = SubscribeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid() and form.cleaned_data:
        subscriber, created = Subscriber.objects.get_or_create(email=request.POST.get('email'), defaults={'first_name': request.POST.get('name')})
        if not created:
            subscriber.status = Subscriber.STATUSES.SUBSCRIBED
            subscriber.save()
        status = 'ok'
    return {'form': form, 'status': status}


@render_to('unsubscribe.html')
def deactivate(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        action = request.GET.get('act')
        if action == 'confirm':
            subscriber = get_object_or_404(Subscriber, email=email)
            subscriber.status = Subscriber.STATUSES.UNSUBSCRIBED
            subscriber.save()
        return {'email': email, 'action': action}
