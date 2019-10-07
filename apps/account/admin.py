from django.contrib import admin
from django.contrib.auth.models import User, Group

from models import Profile, SocialAccount,ExtendedProfile
# from south.models import MigrationHistory


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'presence')
    search_fields = ('user__username', 'user__email')


class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'internal_user_id')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(ExtendedProfile)
admin.site.register(SocialAccount, SocialAccountAdmin)
#admin.site.register(Group)
#admin.site.register(User)
# admin.site.register(MigrationHistory)
