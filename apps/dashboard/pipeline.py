#!/usr/bin/python
# -*- coding: utf-8 -*-
from apps.dashboard.models import UserProfile#, SocialUser

def get_profile_picture(backend, user, response, details, is_new=False, *args, **kwargs ):
    img_url = ""
    if backend.name == 'facebook':
        img_url = '//graph.facebook.com/%s/picture?type=large' \
            % response['id']
    elif backend.name == 'twitter':
        img_url = response.get('profile_image_url', '').replace('_normal', '')
    elif backend.name == 'vk-oauth2':
        img_url = response.get('photo', '').replace('_normal', '')
    elif backend.name == 'google-oauth2':
        img_url = response['image'].get('url')
    profile = UserProfile.objects.get_or_create(user = user)[0]
    profile.photo = img_url
    profile.save()
