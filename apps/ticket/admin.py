# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'submitted_date', 'submitter',
                    'submitted_date', 'modified_date')
    search_fields = ('title', 'description',)

admin.site.register(Ticket, TicketAdmin)
