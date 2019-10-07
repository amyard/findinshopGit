# -*- coding: utf-8
import json
import urllib
import logging
from datetime import datetime, timedelta

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from apps.account.models import SocialAccount
from utils.decorators import render_to

logger = logging.getLogger('airsoft')

class VkontakteBackend(object):
    def authenticate(self, user_id, access_token):
        try:
            sa = SocialAccount.objects.get(internal_user_id=user_id, access_token=access_token)
            return sa.user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

def callback(request):
    logger.info('Request from VK')
    if request.GET.get('code'):
        code = request.GET['code']
        redirect_uri = 'http://%s%s' % (Site.objects.get_current().domain, reverse('oauth2_vk_callback'))
        next = request.GET.get('next') or '/'
        if request.GET.get('next'):
            redirect_uri += '?next=%s' % next
        logger.info('Get access_token, redirect_url=%s' % redirect_uri)
        params = urllib.urlencode({'client_id': settings.VK_APP_ID, 'client_secret': settings.VK_APP_SECRET, 'code': code, 'redirect_uri':redirect_uri})
        f = urllib.urlopen("https://oauth.vk.com/access_token?%s" % params)
        response = json.loads(f.read())
        if response.get('access_token'):
            access_token = response.get('access_token')
            expires = response.get('expires_in')
            user_id = response.get('user_id')
            logger.info('Got access_token for user %s' % user_id)
            password = User.objects.make_random_password()
            try:
                sa = SocialAccount.objects.get(internal_user_id=user_id, social_network=SocialAccount.SOCIAL_NETWORK.VKONTAKTE)
                sa.access_token = access_token
                sa.access_token_expire = datetime.now() + timedelta(seconds=int(expires))
                sa.save()
                logger.info('Authenticate user %s' % user_id)
                user = authenticate(user_id=sa.internal_user_id, access_token=sa.access_token)
                logger.info('Login user %s' % user_id)
                login(request, user)
                if next:
                    logger.info('Redirect user %s to %s' % (user_id, next))
                    return HttpResponseRedirect(next)
                if user.profile.city:
                    return HttpResponseRedirect(reverse('city_page', kwargs={'city_slug':user.profile.city.slug}))
                return HttpResponseRedirect(reverse('account_page', kwargs={'uid':user.id}))
            except SocialAccount.DoesNotExist:
                # get user info
                params = urllib.urlencode({'uids':user_id,'fields':'uid,first_name,last_name,nickname,screen_name,bdate,city,country', 'access_token':access_token})
                f = urllib.urlopen("https://api.vk.com/method/users.get?%s" % params)
                response = json.loads(f.read())
                if request.user.is_authenticated():
                    user = request.user
                else:
                    logger.info('Create new user %s' % user_id)
                    user = User.objects.create(username=response['response'][0].get('screen_name') or response['response'][0].get('nickname'), \
                        first_name=response['response'][0].get('first_name'),  last_name=response['response'][0].get('last_name'))
                    user.set_password(password)
                    user.save()
                sa = SocialAccount.objects.create(user=user, internal_user_id=user_id, \
                        social_network=SocialAccount.SOCIAL_NETWORK.VKONTAKTE, access_token=access_token, \
                        access_token_expire=datetime.now() + timedelta(seconds=int(expires)))
                if not request.user.is_authenticated():
                    logger.info('Authenticate user %s' % user_id)
                    user = authenticate(user_id=sa.internal_user_id, access_token=sa.access_token)
                    logger.info('Login user %s' % user_id)
                    login(request, user)
                if next:
                    logger.info('Redirect user %s to %s' % (user_id, next))
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse('account_page', kwargs={'uid':user.id}))
        elif response.get('error'):
            error = response.get('error')
            description = response.get('error_description')
            logger.error('Access token wasn\'t get %s' % json.dumps(response))
            return HttpResponseRedirect(next)
    elif request.GET.get('error'):
        error = request.GET['error']
        description = request.GET.get('error_description')
        logger.error('Code wasn\'t get %s' % json.dumps(response))
        return HttpResponseRedirect(next)
    return HttpResponseRedirect(reverse('index'))


