# -*- coding: utf-8

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from utils.decorators import render_to
from utils.utils import set_paginator_window

from apps.news.models import News
from forms import NewsForm


@login_required
@render_to('news.html')
def news(request):
    try:
        site_obj = request.user.website
    except Exception:
        site_obj = None
    if site_obj:
        site_news = News.objects.filter(website=site_obj)
        p = Paginator(site_news, 10)
        try:
            page = p.page(request.GET.get('p', 1))
        except PageNotAnInteger:
            page = p.page(1)
        except EmptyPage:
            page = p.page(p.num_pages)
        set_paginator_window(page)
        return {'site_news': site_news, 'page': page}
    else:
        return {}


@login_required
@render_to('news_control.html')
def news_add(request):
    form = NewsForm()
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.website = request.user.website
            inst.save()
            return redirect('news')
    return {'form': form, 'act': 'add'}


@login_required
@render_to('news_control.html')
def news_edit(request, news_id):
    news_obj = get_object_or_404(News, id=news_id, website=request.user.website)
    form = NewsForm(instance=news_obj)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news_obj)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.website = request.user.website
            inst.save()
            return redirect('news')
    return {'form': form, 'act': 'edit'}


@login_required
def news_delete(request, news_id):
    get_object_or_404(News, id=news_id, website=request.user.website).delete()
    return redirect('news')
