#-*- coding: utf-8 -*-
from django.contrib import admin

from models import Message, MessageItem

class MessageItemInline(admin.StackedInline):
    model = MessageItem
    extra = 0

class MessageAdmin(admin.ModelAdmin):
    list_display = ['key', 'date']
    inlines = [MessageItemInline,]

admin.site.register(Message, MessageAdmin)
