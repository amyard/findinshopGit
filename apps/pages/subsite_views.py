# -*- coding: utf-8

from django.shortcuts import get_object_or_404

from apps.pages.models import Page

from utils.decorators import r_to


@r_to('page.html')
def page(request, page_id):
    page = get_object_or_404(Page, id=page_id, website=request.website)
    return {'page': page}
