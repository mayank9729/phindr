
from django.urls import path
from .views import (
    PropertyViewSet,
    FavoriteViewSet,
    SavedSearchViewSet,
    ViewingHistoryViewSet,
    PropertyNoteViewSet,
    SharedPropertyViewSet,
    AmenityViewSet,
)

urlpatterns = [
    path("amenties/", AmenityViewSet.as_view({"get": "list","post":"create"}), name="amenty-list"),
    path("amenties/<int:pk>/", AmenityViewSet.as_view({"patch": "update","delete":"destroy","get":"retrieve"}), name="amenty-list"),
 
    
    path("properties/", PropertyViewSet.as_view({"get": "list","post":"create"}), name="property-list"),
    path("properties/<int:pk>/", PropertyViewSet.as_view({"get": "retrieve"}), name="property-detail"),

    path("favorites/", FavoriteViewSet.as_view({"get": "list", "post": "create"}), name="favorite-list"),
    path("favorites/<int:pk>/", FavoriteViewSet.as_view({"get": "retrieve", "delete": "destroy"}), name="favorite-detail"),

    path("saved-searches/", SavedSearchViewSet.as_view({"get": "list", "post": "create"}), name="savedsearch-list"),
    path("saved-searches/<int:pk>/", SavedSearchViewSet.as_view({"get": "retrieve", "delete": "destroy"}), name="savedsearch-detail"),

    path("viewing-history/", ViewingHistoryViewSet.as_view({"get": "list", "post": "create"}), name="viewinghistory-list"),
    path("viewing-history/<int:pk>/", ViewingHistoryViewSet.as_view({"get": "retrieve"}), name="viewinghistory-detail"),

    path("property-notes/", PropertyNoteViewSet.as_view({"get": "list", "post": "create"}), name="propertynote-list"),
    path("property-notes/<int:pk>/", PropertyNoteViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}), name="propertynote-detail"),

    path("shared-properties/", SharedPropertyViewSet.as_view({"get": "list", "post": "create"}), name="sharedproperty-list"),
    path("shared-properties/<int:pk>/", SharedPropertyViewSet.as_view({"get": "retrieve"}), name="sharedproperty-detail"),
] 
