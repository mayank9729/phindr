from django.contrib import admin
from .models import Property,ViewingHistory

class PropertyAdmin(admin.ModelAdmin):
    list_display = ['id','title','price','address']
    list_filter = ['title', 'price']
    search_fields = ['title', 'price', 'address', ]
admin.site.register(Property, PropertyAdmin)

class ViewingHistoryAdmin(admin.ModelAdmin):
    list_display = ['id','user','property','viewed_at']
    list_filter = ['id', 'user']
    search_fields = ['id', 'user' ]
admin.site.register(ViewingHistory, ViewingHistoryAdmin)


