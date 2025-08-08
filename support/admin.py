from django.contrib import admin
from .models import SupportTicket
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['id','ticket_id','status']
    list_filter = ['id','ticket_id','date']
    search_fields = ['ticket_id' ]
admin.site.register(SupportTicket, SupportTicketAdmin)
