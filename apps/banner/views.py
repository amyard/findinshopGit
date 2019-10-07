from django.contrib.auth.decorators import login_required
from utils.decorators import render_to
from models import Banner

SERVER_URL = 'http://findinshop.com'

@render_to('get.html')
def get(request, user_id=0):
    return {'banner':Banner.objects.filter().order_by('?')[0], 'server_url':SERVER_URL}

