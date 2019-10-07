from django.contrib import admin

from models import Website, UserSpace, WebsiteProperty, Point


class WebsiteAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['subdomain']
        else:
            return []


class PointAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'address', 'city', 'street', 'on_map')


admin.site.register(Website)
admin.site.register(WebsiteProperty)
admin.site.register(UserSpace)
admin.site.register(Point, PointAdmin)
