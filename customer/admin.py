from django.contrib import admin
from .models import User,LicenceCode

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name','email', 'phone', 'is_active', 'is_staff', 'is_admin', 'token','unique_id', 'update_at', 'created_at']
    list_filter = ['is_active', 'is_staff', 'is_admin']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'unique_id']
admin.site.register(User, CustomerAdmin)


class LicenceCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'licence','team_id','uuid','is_deleted','is_active','created_at',]
    list_filter = ['user', 'licence',]
    search_fields = ['user', 'licence']
admin.site.register(LicenceCode, LicenceCodeAdmin)