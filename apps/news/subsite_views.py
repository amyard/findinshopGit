# -*- coding: utf-8

from django.shortcuts import get_object_or_404

from apps.news.models import News

from utils.decorators import r_to


@r_to('news.html')
def news(request, news_id):
    entry = get_object_or_404(News, id=news_id, website=request.website)
    return {'entry': entry}


@r_to('news.html')
def news_all(request):
    news = News.objects.filter(website=request.website)
    return {'news': news}
