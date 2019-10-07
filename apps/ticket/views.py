# -*- coding: utf-8

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import datetime
from utils.decorators import render_to

from apps.ticket.models import Ticket
from forms import TicketForm


def set_paginator_window(page, window=10):
    if page.number < window/2:
        page.paginator.pages_window = range(1, page.paginator.num_pages+1)
    elif page.number > page.paginator.num_pages-window/2:
        page.paginator.pages_window = range(page.paginator.num_pages+1-window, page.paginator.num_pages+1)
    else:
        page.paginator.pages_window = range(page.number-window/2+1, page.number+window/2+1)


@login_required
@render_to('tickets.html')
def tickets(request):
    if request.user.is_staff:
        tickets = Ticket.objects.filter().order_by('status', '-modified_date')
    else:
        tickets = Ticket.objects.filter(submitter=request.user).order_by('status', '-modified_date')
    p = Paginator(tickets, 10)
    try:
        page = p.page(request.GET.get('p', 1))
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)
    set_paginator_window(page)
    return {'tickets': tickets, 'page': page}


@login_required
@render_to('ticket.form.html')
def ticket_add(request):
    form = TicketForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        inst = form.save(commit=False)
        inst.submitter = request.user
        inst.save()
        return redirect('tickets')
    return {'form': form, 'action': 'add'}


@login_required
@render_to('ticket.form.html')
def ticket_control(request, ticket_id, action):
    inst = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST' and request.POST.get('comment'):
        inst.description = "%s<hr><b>%s</b> [%s]: %s" % (inst.description, request.user, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), request.POST.get('comment'))
        inst.save()
    if request.user.is_staff:
        if action == 'set_open':
            inst.description = u"%s<hr>[%s] Изменение статуса на <b>Открыто</b> пользователем <b>%s</b>." % (inst.description, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), request.user)
            inst.status = inst.STATUS_CODES.OPEN
        elif action == 'set_working':
            inst.description = u"%s<hr>[%s] Изменение статуса на <b>В обработке</b> пользователем <b>%s</b>." % (inst.description, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), request.user)
            inst.status = inst.STATUS_CODES.WORKING
        elif action == 'set_closed':
            inst.description = u"%s<hr>[%s] Изменение статуса на <b>Закрыто</b> пользователем <b>%s</b>." % (inst.description, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), request.user)
            inst.status = inst.STATUS_CODES.CLOSED
        inst.save()
    return {'ticket': inst, 'action': 'v'}
