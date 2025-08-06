from django.contrib import admin
from .models import User,IPAddress

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name','email', 'phone', 'is_active', 'is_staff', 'is_admin', 'token','unique_id', 'update_at', 'created_at']
    list_filter = ['is_active', 'is_staff', 'is_admin']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'unique_id']
admin.site.register(User, CustomerAdmin)

class IPAddressAdmin(admin.ModelAdmin):
    list_display = ['id','ip']
admin.site.register(IPAddress, IPAddressAdmin)
