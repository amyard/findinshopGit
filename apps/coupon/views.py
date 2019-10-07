# -*- coding: utf-8 -*-

#Django imports
from django.views.generic import FormView, ListView, DeleteView
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy

from apps.section.mixins import LoginRequiredMixin
from apps.coupon.forms import CouponForm
from apps.coupon.models import Coupon
from apps.catalog.models import Item, Category
from apps.coupon.utils import send_coupon_message
from apps.catalog.tasks import coupon_apply


class CouponCreateView(LoginRequiredMixin, FormView):
    template_name = 'coupon/create_coupon.html'
    form_class = CouponForm

    def get_context_data(self, *args, **kwargs):
        context = super(CouponCreateView, self).get_context_data(*args, **kwargs)
        if self.request.GET.get('filter', False):
            filters = self.request.GET.get('filter')
            if 'category' in filters:
                context['category'] = Category.objects.get(id=filters.split('=')[1])
            elif filters.startswith('id'):
                context['product'] = Item.objects.get(id=filters.split('=')[1])

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.filters = self.request.GET.get('filter', None)
        self.object.save()
        try:
            # TODO rewrite in celery
            send_coupon_message(self.object)
        except Exception:
            pass

        coupon_apply(self.object)

        messages.success(self.request, u'Купон успешно создан')
        return redirect(reverse('coupons'))


class CouponsView(LoginRequiredMixin, ListView):
    template_name = 'coupon/coupons.html'
    queryset = Coupon.objects.filter(deleted=False)
    context_object_name = 'coupons'

    def get_queryset(self, *args, **kwargs):
        qs = super(CouponsView, self).get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs


class CouponDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'coupon/delete_coupon.html'
    model = Coupon
    success_url = reverse_lazy('coupons')
