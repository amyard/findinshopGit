#-*- coding:utf-8 -*-

from utils.decorators import render_to

from forms import VersionForm


@render_to('version.html')
def version(request):
    form = VersionForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
    return {'form': form}
