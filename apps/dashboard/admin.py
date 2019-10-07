from django.contrib import admin
from django.contrib.auth.models import User
# from django.contrib.auth.models import User 
from models import UserProfile,Wishlist,History
# from south.models import MigrationHistory
# from django.contrib.admin.util import flatten_fieldsets
# from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail

def mailto(request,**kwargs):
    if request.method == 'GET':
         return render (request, 'send_email.html',request.GET)
    elif request.method == 'POST': 
        error = []
        if not request.POST.get('topick'): error.append (u"Вы не заполнили тему" )
        if not request.POST.get('txt'): error.append(u"Вы не написали текст письма")
        if error:
            context = {'email':request.POST.get('email'),'topick':request.POST.get('topick'),"txt":request.POST.get('txt'), 'error':error}
            return render (request,'send_email.html',context)
        else:
            email = request.POST.get('email').split(",")
            send_mail(request.POST.get('topick'), request.POST.get('txt'),'test.rborodinov@gmail.com',email, fail_silently=False)
            return HttpResponseRedirect("/admin/dashboard/userprofile/")
    else: return HttpResponseRedirect("/admin/dashboard/userprofile/")



class UserProfileAdmin(admin.ModelAdmin):
    model = User()    
    # search_fields = ['phone']
    list_display = ["email","phone",'country','city',"first_name","last_name"]
    list_filter = ('country','city',"phone",)
    actions = ['send_email']

    def send_email(self, request, queryset):
        emails = set()
        if queryset:
            for profile in queryset:
                emails.add(profile.user.email)

        url = "/admin/mailto?email={}".format(",".join(emails))
        return HttpResponseRedirect ( url )


class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = ('item', 'user')
    # readonly_fields = Wishlist._meta.get_all_field_names()
    def has_add_permission(self, request):
        return False
        
admin.site.register(UserProfile, UserProfileAdmin)
# admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Wishlist,ReadOnlyAdmin)
admin.site.register(History,ReadOnlyAdmin)
