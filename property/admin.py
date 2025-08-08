from django.contrib import admin
from .models import Property,ViewingHistory,Amenity,Favorite,SavedSearch,PropertyNote,SharedProperty

class AmenityAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    list_filter = ['name']
    search_fields = ['name']
admin.site.register(Amenity, AmenityAdmin)


class PropertyAdmin(admin.ModelAdmin):
    list_display = ['id','title','price','address']
    list_filter = ['title', 'price']
    search_fields = ['title', 'price', 'address', ]
admin.site.register(Property, PropertyAdmin)

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id','user']
    list_filter = ['user']
    search_fields = ['user' ]
admin.site.register(Favorite, FavoriteAdmin)

class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ['id','user']
    list_filter = ['user']
    search_fields = ['user' ]
admin.site.register(SavedSearch, SavedSearchAdmin)

class ViewingHistoryAdmin(admin.ModelAdmin):
    list_display = ['id','user','property','viewed_at']
    list_filter = ['id', 'user']
    search_fields = ['id', 'user' ]
admin.site.register(ViewingHistory, ViewingHistoryAdmin)

class PropertyNoteAdmin(admin.ModelAdmin):
    list_display = ['id','user','personal_rating']
    list_filter = ['user','personal_rating']
    search_fields = ['user','personal_rating' ]
admin.site.register(PropertyNote, PropertyNoteAdmin)

class SharedPropertyAdmin(admin.ModelAdmin):
    list_display = ['id','user','co_applicant_email']
    list_filter = ['user','co_applicant_email']
    search_fields = ['user','co_applicant_email' ]
admin.site.register(SharedProperty, SharedPropertyAdmin)