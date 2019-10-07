from django.contrib import admin
from models import (
    Category,
    Item,
    Catalog,
    ItemVideo,
    ImportTask,
    ExportTask,
    Order,
    OrderItem,
    CurrencyRate,
    Vendor
)


class CurrencyPairInline(admin.TabularInline):
    model = CurrencyRate
    extra = 0


class CatalogAdmin(admin.ModelAdmin):
    inlines = (CurrencyPairInline,)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('site', 'name', 'click_cost', 'category')
    list_display_links = ('site', 'name')
    list_filter = ('site',)
    readonly_fields = ('click_cost',)
    search_fields = ['name']


class CategoryAdmin(admin.ModelAdmin):
    # fields = '__all__'
    list_display = ('name', 'parent', 'catalog', 'deleted')
    list_filter = ('catalog', 'deleted')


class ImportTaskAdmin(admin.ModelAdmin):
    list_display = ('catalog', 'format', 'start', 'complete', 'status', 'validity')
    list_filter = ('validity', 'status', 'format',)

    class Media:
        js = ('/static/themes/findinshop/js/admin/adminfix.js', )

# admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(ItemVideo)
admin.site.register(ImportTask, ImportTaskAdmin)
admin.site.register(ExportTask)
admin.site.register(Vendor)
