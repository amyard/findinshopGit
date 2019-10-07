from django.shortcuts import render, render_to_response
from utils2.decorators import render_to
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from social.apps.django_app.default.models import UserSocialAuth
from apps.dashboard.models import UserProfile, Wishlist, History
from apps.catalog.models import Item
from apps.dashboard.forms import UserForm, UserAutentication
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from ipware.ip import get_ip
from pygeoip import GeoIP
import json
import requests
import source.settings


def handle_uploaded_file(f, uid):
    name = f.name
    path = '{}/user_photo/{}.{}'.format(settings.MEDIA_ROOT, uid, name.split('.')[-1])
    print path
    with open(path, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
    return '{}user_photo/{}.{}'.format(settings.MEDIA_URL, uid, name.split('.')[-1])


def register_user(request):
    context_dict = {}
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        context_dict['user_form'] = user_form
        if user_form.is_valid():
            print request.POST
            print user_form.cleaned_data
            user = user_form.save()
            password = user.password
            user.set_password(user.password)
            user.save()
            profile_form = UserProfile()
            profile_form.user = user
            profile_form.save()
            if 'photo' in request.FILES:
                profile_form.photo = handle_uploaded_file(request.FILES['photo'], request.user.id)
                profile_form.save()
            user = authenticate(username=user.username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
        else:
            render(request, 'register_user.html', context_dict)
    # elif request.user.is_active:
    #     return HttpResponseRedirect('/dashboard/')
    else:
        user_form = UserForm()
        context_dict['user_form'] = user_form
    return render(request, 'register_user.html', context_dict)


class LoginFormView(FormView):
    form_class = UserAutentication
    template_name = 'login_user.html'
    success_url = '/dashboard/'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


def geolocation(request):
    if request.user.is_authenticated():
        profile = UserProfile.objects.get(user=request.user)
        if profile.latitude == None:
            latitude, longitude, country, city = None, None, None, None
            if 'latitude' in request.GET:
                latitude = request.GET.get('latitude')
                longitude = request.GET.get('longitude')
                url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&language=ru&key={2}'.format(
                    latitude, longitude, settings.GEOCODING_API_KEY)
                response = requests.get(url)
                data = json.loads(response.content)
                components = data["results"][2]["address_components"]
                # while not (country and city):# maybe need to search in data["results"][1]["address_components"] and other???
                for item in components:
                    if item["types"] == ['country', 'political']:
                        country = item["long_name"]
                    if item["types"] == ['locality', 'political']:
                        city = item["long_name"]
            if 'error' in request.GET:
                ip = get_ip(request)
                gi = GeoIP(settings.GEO_LITE_CITY_PATH)
                gir = gi.record_by_addr(ip)
                # to get location data by IP on russian language we can send reqests to url: requests.get(url)  url= http://ip-api.com/json/{}?fields=209&lang=ru.format(ip)
                if gir is not None:
                    latitude = gir['latitude']
                    longitude = gir['longitude']
                    country = gir['country_name']
                    city = gir['city']
            if latitude: profile.latitude = latitude
            if longitude: profile.longitude = longitude
            if country: profile.country = country
            if city: profile.city = city
            profile.save()
            return HttpResponse(
                json.dumps({'latitude': latitude, 'longitude': longitude, 'country': country, 'city': city}))
    return render(request, '404.html')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@render_to('history.html')
def test(request):
    wishlist = 0
    print
    return ({"wishlist": wishlist})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/dashboard")


@render_to('dashboard.html')
def dashboard(request):
    # print get_client_ip(request)
    context_dict = {}
    context_dict['user'] = request.user
    user = request.user
    profile, social, history, wishlist = None, None, None, None
    # print user.get_social_auth()s
    try:
        profile = UserProfile.objects.get(user=request.user)
        social = UserSocialAuth.objects.get(user=request.user)
    except Exception:
        pass
    try:
        history = History.objects.filter(user=user)[::-1]
        wishlist = Wishlist.objects.filter(user=user)[::-1]

    except Exception:
        pass
    if history:
        lenght = len(history)
        if lenght > 30:
            for item in history[30:lenght]:
                item.delete()
        if lenght > 10:
            history = history[0:10]
    context_dict['profile'] = profile
    context_dict['social'] = social
    context_dict['history'] = history
    context_dict['wishlist'] = wishlist
    return (context_dict)


class HistoryView(ListView):
    template_name = ('history.html')
    # model_class = Item
    # paginate_by = 25

    def get_queryset(self):
        if self.request.user.is_active:
            if 'history' in self.args:
                queryset = History.objects.filter(user=self.request.user).order_by('-id')
            elif 'wishlist' in self.args:
                queryset = Wishlist.objects.filter(user=self.request.user).order_by('-id')
        else:
            queryset = list()
        return queryset