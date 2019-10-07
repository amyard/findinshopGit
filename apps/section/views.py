# -*- coding: utf-8 -*-

# Python imports
import json

# Django imports

from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404

# findinshop imports
from apps.section.models import Section, ProductModel, Parameter
from apps.section.utils import create_parameter_filter, create_parameters_list, create_parameter_string
from apps.section.mixins import AdminMixin
from apps.catalog.tasks import parse_hotline_items

ALLOWED_KEYS_DICT = {'1': 'rating', '2': 'price_min', '3': '-price_min'}


class SectionView(ListView):
    template_name = 'section/sections.html'
    model = Section
    context_object_name = 'sections'

    def get(self, request, *args, **kwargs):
        if 'next' in request.GET:
            return redirect(to='/'+request.GET['next'])

        return super(SectionView, self).get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(SectionView, self).get_queryset(*args, **kwargs)
        if not self.kwargs:
            qs = qs.filter(parent__isnull=True)
        else:
            qs = qs.filter(parent__slug=self.kwargs['slug'])
        return qs


    def get_context_data(self, *args, **kwargs):
        context = super(SectionView, self).get_context_data(*args, **kwargs)
        if 'slug' in self.kwargs:
            if 'filter_setting' in self.request.session:
                filter_mode = True
            else:
                filter_mode = False
            try:
                section = get_object_or_404(Section, slug=self.kwargs['slug'])
            except Http404:
                qs = get_object_or_404(ProductModel, slug=self.kwargs['slug'])
                context['product_model'] = qs
                return context

            products = ProductModel.objects.filter(section=section)

            parameters = create_parameters_list(self.kwargs)
            if parameters:
                products = products.filter(*create_parameter_filter(parameters))

            if self.request.GET.get('sort', '1'):
                if self.request.GET.get('sort') in ALLOWED_KEYS_DICT.keys():
                    products = products.order_by(ALLOWED_KEYS_DICT[self.request.GET.get('sort')])

            context['section'] = section
            context['filters'] = create_parameters_list(self.kwargs)
            context['count_in_page'] = int(self.request.GET.get('count_in_page', 20))
            context['sort'] = self.request.GET.get('sort', '1')
            context['filter_mode'] = filter_mode
            context['products'] = products

        return context


class ProductView(ListView):
    template_name = 'section/products.html'
    model = ProductModel
    context_object_name = 'products'

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get('add', False):
            if 'filters' in kwargs:
                filters = '%s-%s' % (kwargs['filters'], request.GET.get('add'))
            else:
                filters = int(request.GET.get('add'))
            return redirect(reverse('products', kwargs={'slug': kwargs['slug'], 'filters': filters}))

        if request.GET.get('remove', False) and 'filters' in kwargs:
            filters = create_parameters_list(kwargs)
            if int(request.GET.get('remove')) in filters:
                filters.remove(int(request.GET.get('remove')))
            if create_parameter_string(filters):
                return redirect(
                    reverse('products', kwargs={'slug': kwargs['slug'], 'filters': create_parameter_string(filters)}))
            else:
                return redirect(reverse('products', kwargs={'slug': kwargs['slug']}))

        return super(ProductView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductView, self).get_queryset(*args, **kwargs)
        section = get_object_or_404(Section, slug=self.kwargs['slug'])
        # qs = section.get_all_items()
        qs = ProductModel.objects.filter(section=section)

        parameters = create_parameters_list(self.kwargs)
        if parameters:
            qs = qs.filter(*create_parameter_filter(parameters))

        if self.request.GET.get('sort', '1'):
            if self.request.GET.get('sort') in ALLOWED_KEYS_DICT.keys():
                qs = qs.order_by(ALLOWED_KEYS_DICT[self.request.GET.get('sort')])
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(ProductView, self).get_context_data(*args, **kwargs)

        if 'filter_setting' in self.request.session:
            filter_mode = True
        else:
            filter_mode = False

        context['section'] = get_object_or_404(Section, slug=self.kwargs['slug'])
        context['filters'] = create_parameters_list(self.kwargs)
        context['count_in_page'] = int(self.request.GET.get('count_in_page', 20))
        context['sort'] = self.request.GET.get('sort', '1')
        context['filter_mode'] = filter_mode

        return context


class ProductSetView(DetailView):
    template_name = 'section/product_set.html'
    model = ProductModel
    context_object_name = 'product_model'


class AdminJsonParameterView(AdminMixin, ListView):
    queryset = Parameter.objects.all()

    def get_queryset(self, *args, **kwargs):
        qs = super(AdminJsonParameterView, self).get_queryset(*args, **kwargs)
        if not self.kwargs.get('feature_id'):
            qs = Parameter.objects.none()
        else:
            qs = qs.filter(features=self.kwargs.get('feature_id'))

        return qs

    def render_to_response(self, context):
        parameters = self.object_list
        parameter_list = []
        for parameter in parameters:
            parameter_list.append({'id': parameter.pk, 'name': parameter.name})

        return HttpResponse(json.dumps(parameter_list), content_type='application/json')


@login_required
def parse_hotline(request):
    url = request.GET['parse']
    section_id = request.GET['section_id']
    parse_hotline_items(url, section_id)
    try:
        #parse_hotline_items.delay(url, section_id)


        result = {'result': 'ok'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    except:
        return HttpResponse('failure', status=400)

