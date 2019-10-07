# -*- coding: utf-8

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from utils.decorators import render_to
from utils.utils import set_paginator_window

from apps.pages.models import Page
from forms import PageForm


@login_required
@render_to('pages.html')
def pages(request):
    try:
        site_obj = request.user.website
    except Exception:
        site_obj = None
    if site_obj:
        site_pages = Page.objects.filter(website=site_obj)
        p = Paginator(site_pages, 10)
        try:
            page = p.page(request.GET.get('p', 1))
        except PageNotAnInteger:
            page = p.page(1)
        except EmptyPage:
            page = p.page(p.num_pages)
        set_paginator_window(page)
        return {'site_pages': site_pages, 'page': page}
    else:
        return {}


@login_required
@render_to('pages_control.html')
def pages_add(request):
    if request.user.website.pages.count() < 8:
        form = PageForm()
        if request.method == 'POST':
            form = PageForm(request.POST)
            if form.is_valid():
                inst = form.save(commit=False)
                inst.website = request.user.website
                inst.save()
                return redirect('pages')
        return {'form': form, 'act': 'add'}
    else:
        return redirect('pages')


@login_required
@render_to('pages_control.html')
def pages_edit(request, page_id):
    page_obj = get_object_or_404(Page, id=page_id, website=request.user.website)
    form = PageForm(instance=page_obj)
    if request.method == 'POST':
        form = PageForm(request.POST, instance=page_obj)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.website = request.user.website
            inst.save()
            return redirect('pages')
    return {'form': form, 'act': 'edit'}


@login_required
def pages_delete(request, page_id):
    get_object_or_404(Page, id=page_id, website=request.user.website).delete()
    return redirect('pages')
