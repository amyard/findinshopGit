# -*- coding: utf-8 -*-

#Python imports
import json
import datetime

#Django imports
from django.views.generic import View, CreateView, ListView, FormView, RedirectView, UpdateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.cache import cache

#findinshop imports
from apps.cpa.models import CostSetting, Report, OwnAndUserCategory
from apps.cpa.helpers import get_caterogy_with_cost
from apps.cpa.forms import CategoryCostForm, ReportClickForm
from apps.cpa.decorators import transition_action
from apps.cpa.utils import get_item_unique_cookie_key, get_report_cookie_key
from apps.cpa.decorators import transition_action
from apps.cpa.tasks import export_report

from apps.section.models import Section
from apps.section.mixins import LoginRequiredMixin
from apps.section.utils import get_obj_or_none
from apps.catalog.models import Item
from apps.account.models import Profile
from apps.catalog.models import Catalog, Category
from apps.website.models import Website
from apps.catalog.tasks import refresh_cost


CACHE_TIMEOUT_REPORT = 2*3600 #2 hours


class CostSettingView(LoginRequiredMixin, FormView):
    template_name = 'cpa/cost_setting.html'
    form_class = CategoryCostForm

    def get(self, *args, **kwargs):
        self.form_class.user = self.request.user
        return super(CostSettingView, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(CostSettingView, self).get_context_data(*args, **kwargs)
        sections = Section.parents.all()
        for section in sections:
            cost_setting = CostSetting.objects.filter(user=self.request.user, section=section)
            if cost_setting:
                section.base_cost = cost_setting[0].base_cost
                section.current_rate = cost_setting[0].current_rate
                section.total_cost = cost_setting[0].total_cost
            else:
                section.base_cost = 0
                section.current_rate = 0
                section.total_cost = 0

        context['sections'] = sections

        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        setting = get_object_or_404(CostSetting, user=self.request.user, section=cleaned_data['section'])

        setting.current_rate=cleaned_data['current_rate']
        setting.total_cost=setting.base_cost + setting.current_rate
        setting.changed = True
        setting.save()

        #re-price cost click for products
        refresh_cost(setting)

        messages.success(self.request, u'Ставка для раздела "%s" успешно изменена' % setting.section.name)
        return redirect(reverse('cost_setting'))


class ReportClickView(LoginRequiredMixin, ListView):
    queryset = Report.objects.none()
    template_name = 'cpa/report_click.html'
    context_object_name = 'reports'
    report_key = None

    def get_context_data(self, *args, **kwargs):
        context = super(ReportClickView, self).get_context_data(*args, **kwargs)
        context['form'] = ReportClickForm(self.request.GET or None)
        context['from'] = self.request.GET.get('date_from', None)
        context['to'] = self.request.GET.get('date_to', None)
        context['report_key'] = self.report_key

        return context

    def get_queryset(self, *args, **kwargs):
        form = ReportClickForm(self.request.GET or None)
        #import pdb;pdb.set_trace()
        if form.is_valid():
            data = form.cleaned_data
            report_key = get_report_cookie_key(self.request.user, data['date_from'], data['date_to'])
            #save self report key
            self.report_key = report_key

            if not cache.get(report_key, False):
                self.queryset = Report.objects.filter(user=self.request.user, date__gte=data['date_from'], date__lte=data['date_to'])
                cache.set(report_key, self.queryset, CACHE_TIMEOUT_REPORT)
            else:
                self.queryset = cache.get(report_key)

        return super(ReportClickView, self).get_queryset(*args, **kwargs)


class ReportClickXMLView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        report_key_separate = self.kwargs['report_key'].split('_')
        report_key = '%s_%s_%s_%s' % (report_key_separate[0], self.request.user.id, report_key_separate[2], report_key_separate[3])

        #TODO: excel file create
        return export_report(report_key)

        url = '%s?date_from=%s&date_to=%s' % (reverse('report_click'), report_key_separate[2], report_key_separate[3])
        return redirect(url)


class TransitionView(RedirectView):

    def get(self, *args, **kwargs):
        #super(TransitionView, self).get(self, *args, **kwargs)
        try:
            item = Item.objects.get(pk=kwargs['product_id'])
        except:
            return redirect('http://findinshop.com/')

        #TODO: Сделать отдельную страницу для продуктов с пустым урлом
        #1c магазин
        if item.one_c:
            self.url = 'http://findinshop.com/'
        else:
            self.url = item.get_url()

        if not self.url:
            self.url = 'http://findinshop.com/'

        cookie_item_key = get_item_unique_cookie_key(item)
        ip = self.request.META.get('REMOTE_ADDR', None)

        if not cookie_item_key in self.request.COOKIES:
            own_category = OwnAndUserCategory.objects.filter(site=item.site, categories__id=item.category.id)
            report = Report(
                    user=item.site.user,
                    section=own_category[0].our_section if own_category else None,
                    category=item.category,
                    product_name=item.name[:255],
                    cost=item.click_cost,
                    ip=ip
                )
            report.save()

            #paid for click
            profile = get_obj_or_none(Profile, user=report.user)
            if profile:
                profile.balance -= report.cost
                profile.save()

        return self.post(*args, **kwargs)

    @transition_action
    def post(self, *args, **kwargs):
        return redirect(self.url)


class JsonCategoryCostView(LoginRequiredMixin, ListView):
    queryset = Section.objects.none()

    def get_queryset(self, *args, **kwargs):
        if 'section_id' in self.kwargs:
            parent_section = get_object_or_404(Section, pk=self.kwargs['section_id'])
            children = parent_section.get_children_from_parent()
            qs = get_caterogy_with_cost(self.request.user, children)
            return qs
        else:
            return super(JsonCategoryCostView, self).get_query_set(*args, **kwargs)

    def render_to_response(self, context):
        category_list = []
        for category in self.object_list:
            category_list.append({
                        'id': category.pk,
                        'name': category.name,
                        'parent_pk': self.kwargs['section_id'],
                        'count_item': category.count_item,
                        'base_cost': category.base_cost,
                        'current_rate': category.current_rate,
                        'total_cost': category.total_cost
                })

        return HttpResponse(json.dumps(category_list), content_type='application/json')


class JsonUserCategoryBySiteView(LoginRequiredMixin, ListView):
    queryset = Category.objects.none()

    def get_queryset(self, *args, **kwargs):
        if 'site_id' in self.kwargs:
            site = get_object_or_404(Website, id=self.kwargs['site_id'])
            catalog = get_object_or_404(Catalog, website=site)

            fixed_category = []
            for obj in OwnAndUserCategory.objects.filter(site=site):
                for cat in obj.categories.all():
                    fixed_category.append(cat.pk)

            qs = Category.objects.filter(catalog=catalog).exclude(pk__in=fixed_category)
            return qs
        else:
            return super(JsonUserCategoryBySiteView, self).get_queryset(*args, **kwargs)

    def render_to_response(self, context):
        category_list = []
        for category in self.object_list:
            category_list.append({
                        'id': category.pk,
                        'name': category.name,
                })

        return HttpResponse(json.dumps(category_list), content_type='application/json')


class EditCostView(LoginRequiredMixin, UpdateView):

    def get(self, *args, **kwargs):
        get_data = self.request.GET.copy()
        get_data.update({'user': self.request.user})
        form = CategoryCostForm(get_data)
        answer = {}

        if form.is_valid():
            setting = get_object_or_404(CostSetting, user=self.request.user, section=form.cleaned_data['section'])

            setting.current_rate = form.cleaned_data['current_rate']
            setting.total_cost = setting.base_cost + setting.current_rate
            setting.changed = True
            setting.save()

            #Disabled children
            # #refresh cost for all children section
            # for children_section in setting.section.get_children_from_parent():
            #     setting = get_object_or_404(CostSetting, user=self.request.user, section=children_section)

            #     setting.current_rate=form.cleaned_data['current_rate']
            #     setting.total_cost=setting.base_cost + setting.current_rate
            #     setting.changed = True
            #     setting.save()

            #re-price cost click for products
            refresh_cost(setting)
            answer = {
                'status': 'ok',
                'total': setting.total_cost,
                'message': u'Процесс переоценки раздела успешно запущен.'
            }
        else:
            errors = ['%s' % v for k,v in form.errors.items()]
            answer = {'status': 'error', 'message': errors}

        return HttpResponse(json.dumps(answer), content_type='application/json')
