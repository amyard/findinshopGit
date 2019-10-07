#-*- coding:utf-8 -*-

from django.shortcuts import redirect
from utils.decorators import r_to, check_subsite_version
from django.core.mail import send_mail

from mailshelf import messages

from apps.version.models import Version
from models import Message
from forms import FeedbackForm


@r_to('feedback.html')
@check_subsite_version(Version.TYPE.FEEDBACK)
def feedback(request):
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            try:
                msg = Message()
                msg.name = form.cleaned_data['name']
                msg.email = form.cleaned_data['email']
                msg.text = form.cleaned_data['text']
                msg.save()
                send_mail(
                    u'Вопрос с сайта %s' % request.website,
                    u'%s' % msg.text,
                    u'%s' % msg.email,
                    [request.website.user.email],
                    fail_silently=False
                )
                #messages.FEEDBACK_MESSAGE.send(request.website.user.email, **form.cleaned_data)
                status = 1
            except Exception:
                status = 0
            return redirect('feedback_sent', status=status)
    return {'form': form}


@r_to('feedback_sent.html')
@check_subsite_version(Version.TYPE.FEEDBACK)
def feedback_sent(request, status):
    return {'status': status}
