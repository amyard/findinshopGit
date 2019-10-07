# -*- coding: utf-8
import logging
import os

from django.conf import settings as settings_
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# from django.views.generic import FormView, TemplateView, DetailView
from django.utils.http import int_to_base36, base36_to_int
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.mail import mail_managers
from django.views.generic import FormView


from utils2.decorators import render_to
from mailshelf import messages

from models import SocialAccount
from forms import (
    SignupForm,
    SignupForm2,
    SignupForm3,
    ProfileEditForm,
    SignupOnlineMarketForm,
    SignupOfflineMarketForm
)

logger = logging.getLogger('django')


class SignupOnlineMarketFormView(FormView):
    template_name = "themes/findinshop/red/signup_market.html"
    form_class = SignupOnlineMarketForm
    is_online_market = True

    def dispatch(self, request, *args, **kwargs):
        """
        Making sure that only new user can create request
        """
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('account'))
        return super(SignupOnlineMarketFormView, self).dispatch(
            request, *args, **kwargs)

    def form_valid(self, form):
        #
        form = form.save(commit=False)
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('signup_complete2')

    def get_context_data(self, **kwargs):
        context = super(SignupOnlineMarketFormView, self).get_context_data(**kwargs)
        context['is_online_market'] = self.is_online_market
        return context


class SignupOfflineMarketFormView(SignupOnlineMarketFormView):
    form_class = SignupOfflineMarketForm
    is_online_market = False

#@render_to('themes/findinshop/signup.html')
@render_to('themes/findinshop/red/signup.html')
def signup(request):
    try:
        request.user.website
        flag = True
    except Exception:
        flag = False
    if request.user.is_authenticated() and flag:
        return HttpResponseRedirect(reverse('account'))
    initial = {}
    if request.GET.get('i'):
        initial = {'invite': request.GET.get('i')}
    form = SignupForm(initial=initial)
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            #user = User()
            #user.username = form.cleaned_data['email']
            user = form.save()
            #messages.SIGNUP_ACTIVATE.send(user.email, **{'user': user, 'uid': int_to_base36(user.id), 'token': default_token_generator.make_token(user)})
            return HttpResponseRedirect(reverse('signup_complete'))
    return {'form': form}

#@render_to('themes/findinshop/signup2.html')
@render_to('themes/findinshop/red/signup2.html')
def signup2(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account'))
    initial = {}
    if request.GET.get('i'):
        initial = {'invite': request.GET.get('i')}
    form = SignupForm2(initial=initial)
    if request.method == 'POST':
        # form = SignupForm2(data=request.POST)
        form = SignupForm2(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # messages.SIGNUP_ACTIVATE.send(user.email, **{'user': user, 'uid': int_to_base36(user.id), 'token': default_token_generator.make_token(user)})
            #messages.SIGNUP_SEND_MESSAGE.send(user.email, **{'user': user, 'uid': int_to_base36(user.id), 'token': default_token_generator.make_token(user)})
            mail_managers(u'Новая регистрация', u'Был создан новый пользователь для онлайн-магазина %s. Ссылка на прайс: %s' % (user,  user.eprofile.link_XML))
            # for m in settings_.MANAGERS:
            #     messages.SIGNUP_ACTIVATE.send(m[1], **{'user': user, 'uid': int_to_base36(user.id), 'token': default_token_generator.make_token(user)})
            return HttpResponseRedirect(reverse('signup_complete2'))
    return {'form': form}


@render_to('themes/findinshop/red/signup3.html')
def signup3(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account'))
    initial = {}
    if request.GET.get('i'):
        initial = {'invite': request.GET.get('i')}
    form = SignupForm3(initial=initial)

    if request.method == 'POST':
        form = SignupForm3(data=request.POST)
        if form.is_valid():
            user = form.save()
            path = os.path.join(settings_.MEDIA_ROOT, '1c_files/%s' % user.username.lower())
            os.makedirs(path, 777)

            return HttpResponseRedirect(reverse('signup_complete2'))

    return {'form': form}


def activate(request, uidb36=None, token=None):
    try:
        uid_int = base36_to_int(uidb36)
        user = User.objects.get(id=uid_int)
    except (ValueError, User.DoesNotExist):
        user = None

    if user is not None and user.is_active:
        return HttpResponseRedirect(reverse('signup_already_active'))

    if user is not None and default_token_generator.check_token(user, token):
        if request.user.is_authenticated():
            logout(request)
        user.is_active = False
        user.save()
        link = ''
        if user.eprofile.link_XML:
            link = user.eprofile.link_XML
        mail_managers(u'Новая регистрация', u'Был создан новый профиль для пользователя %s. Email: %s, номер телефона: %s, субдомен: %s, ссылка XML: %s' % (user.username, user.email, user.profile.phone_number, user.website.subdomain,link))
        return HttpResponseRedirect(reverse('signup_done'))
    else:
        return HttpResponseRedirect(reverse('signup_invalid_link'))


@login_required
def account(request):
    return HttpResponseRedirect(reverse('account_page', kwargs={'uid': request.user.id}))


@login_required
@render_to('account_page.html')
def account_page(request, uid):
    if uid == str(request.user.id):
        user = request.user
    else:
        user = get_object_or_404(User, id=uid)
    user_content_type = ContentType.objects.get_for_model(User)
    return {'user': user, 'user_content_type': user_content_type}


@login_required
@render_to('account_other.html')
def account_other(request, uid):
    if uid == str(request.user.id):
        user = request.user
    else:
        user = get_object_or_404(User, id=uid)
    return {'user': user}


@login_required
@render_to('settings.html')
def settings(request):
    initial = {'first_name': request.user.first_name, 'last_name': request.user.last_name}
    form = ProfileEditForm(initial=initial, instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, initial=initial, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('account_page', kwargs={'uid': request.user.id}))
    return {'form': form}


@login_required
@render_to('social.html')
def social(request):
    if request.GET.get('d'):
        try:
            request.user.social_accounts.get(social_network=SocialAccount.SOCIAL_NETWORK.VKONTAKTE).delete()
        except SocialAccount.DoesNotExist:
            pass
        return HttpResponseRedirect(reverse('account_social'))
    try:
        vk = request.user.social_accounts.get(social_network=SocialAccount.SOCIAL_NETWORK.VKONTAKTE)
    except SocialAccount.DoesNotExist:
        vk = None
    return {'vk': vk}

