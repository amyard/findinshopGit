from django.contrib import admin

from models import Letter, Subscriber, CouponSubscriber


class LetterAdmin(admin.ModelAdmin):
    # class Media:
    #     js = ('h5bp/js/ckeditor/jquery-1.9.1.min.js', 'h5bp/js/ckeditor/ckeditor.js', 'h5bp/js/ckeditor/apply.js', 'h5bp/js/select_all_m2m.js')

    list_display = ('title', 'date', 'status')
    filter_horizontal = ('recipients',)


class CouponSubscriberAdmin(admin.ModelAdmin):
    model = CouponSubscriber
    list_display = (
        'get_user_information',
        'product_name',
        'product_group',
        'market_name',
        'price'
    )

admin.site.register(Subscriber)
admin.site.register(Letter, LetterAdmin)
admin.site.register(CouponSubscriber, CouponSubscriberAdmin)
