from rest_framework import viewsets, status,filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from core.utils.response_handler import ResponseHandler
from core.utils.exceptions import custom_exception_handler
from .models import *
from .serializers import *
from .filters import PropertyFilter
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Amenity
from .serializers import AmenitySerializer
from rest_framework.permissions import AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class AmenityViewSet(viewsets.ViewSet):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes=[IsAuthenticated]
    def list(self, request):
        amenities = Amenity.objects.all()
        serializer = AmenitySerializer(amenities, many=True)
        return ResponseHandler.success(data=serializer.data)

    def retrieve(self, request, pk=None):
        amenity = get_object_or_404(Amenity, pk=pk)
        serializer = AmenitySerializer(amenity)
        return ResponseHandler.success(data=serializer.data)

    def create(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.success(message="Amenity created", data=serializer.data, status_code=status.HTTP_201_CREATED)
        return ResponseHandler.error(data=serializer.errors)

    def update(self, request, pk=None):
        amenity = get_object_or_404(Amenity, pk=pk)
        serializer = AmenitySerializer(amenity, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.success(message="Amenity updated", data=serializer.data)
        return ResponseHandler.error(data=serializer.errors)

    def destroy(self, request, pk=None):
        amenity = get_object_or_404(Amenity, pk=pk)
        amenity.delete()
        return ResponseHandler.success(message="Amenity deleted")


class PropertyViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_class = PropertyFilter
    search_fields = ['address', 'price',  'title']  
    ordering_fields = ['price',  'title']
        

class FavoriteViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
  #  permission_classes=[AllowAny]
    def list(self, request):
        queryset = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(queryset, many=True)
        return ResponseHandler.success(data=serializer.data)

    def retrieve(self, request, pk=None):
        try:
            favorite = Favorite.objects.get(pk=pk, user=request.user)
            self.check_object_permissions(request, favorite)
            serializer = FavoriteSerializer(favorite)
            return ResponseHandler.success(data=serializer.data)
        except Favorite.DoesNotExist:
            return ResponseHandler.error(message="Not found", status_code=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return ResponseHandler.success(data=serializer.data, status_code=status.HTTP_201_CREATED)
        return ResponseHandler.error(data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            favorite = Favorite.objects.get(pk=pk, user=request.user)
            self.check_object_permissions(request, favorite)
            favorite.delete()
            return ResponseHandler.success(message="Deleted", status_code=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return ResponseHandler.error(message="Not found", status_code=status.HTTP_404_NOT_FOUND)


class SavedSearchViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    def list(self, request):
        queryset = SavedSearch.objects.filter(user=request.user)
        serializer = SavedSearchSerializer(queryset, many=True)
        return ResponseHandler.success(data=serializer.data)

    def retrieve(self, request, pk=None):
        try:
            search = SavedSearch.objects.get(pk=pk, user=request.user)
            self.check_object_permissions(request, search)
            serializer = SavedSearchSerializer(search)
            return ResponseHandler.success(data=serializer.data)
        except SavedSearch.DoesNotExist:
            return ResponseHandler.error(message="Not found", status_code=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = SavedSearchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return ResponseHandler.success(data=serializer.data, status_code=status.HTTP_201_CREATED)
        return ResponseHandler.error(data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            search = SavedSearch.objects.get(pk=pk, user=request.user)
            self.check_object_permissions(request, search)
            search.delete()
            return ResponseHandler.success(message="Deleted", status_code=status.HTTP_204_NO_CONTENT)
        except SavedSearch.DoesNotExist:
            return ResponseHandler.error(message="Not found", status_code=status.HTTP_404_NOT_FOUND)


class ViewingHistoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def list(self, request):
        queryset = ViewingHistory.objects.filter(user=request.user)
        serializer = ViewingHistorySerializer(queryset, many=True)
        return ResponseHandler.success(data=serializer.data)

    def retrieve(self, request, pk=None):
        try:
            history = ViewingHistory.objects.get(pk=pk, user=request.user)
            self.check_object_permissions(request, history[IsAuthenticated, IsOwnerOrReadOnly])
            serializer = ViewingHistorySerializer(history)
            return ResponseHandler.success(data=serializer.data)
        except ViewingHistory.DoesNotExist:
            return ResponseHandler.error(message="Not found", status_code=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = ViewingHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return ResponseHandler.success(data=serializer.data, status_code=status.HTTP_201_CREATED)
        return ResponseHandler.error(data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class PropertyNoteViewSet(viewsets.ViewSet):
    permission_classes =[IsAuthenticated, IsOwnerOrReadOnly]

    def list(self, request):
        queryset = PropertyNote.objects.filter(user=request.user)
        serializer = PropertyNoteSerializer(queryset, many=True)
        return ResponseHandler.success(data=serializer.data)

    def retrieve(self, request, pk=None):
        try:
            note = PropertyNote.objects.get(pk=pk, user=request.user)
            self.check_object_permissions(request, note)
            serializer = PropertyNoteSerializer(note)
            return ResponseHandler.success(data=serializer.data)
        except PropertyNote.DoesNotExist:
            return ResponseHandler.error(message="Not found", status_code=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = PropertyNoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return ResponseHandler.success(data=serializer.data, status_code=status.HTTP_201_CREATED)
        return ResponseHandler.error(data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            note = PropertyNote.objects.get(pk=pk, user=request.user)
            self.check_object_permissions(request, note)
            serializer = PropertyNoteSerializer(note, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseHandler.success(data=serializer.data)
            return ResponseHandler.error(data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
        except PropertyNote.DoesNotExist:
            return ResponseHandler.error(message="Not found", status_code=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            note = PropertyNote.objects.get(pk=pk, user=request.user)
            self.check_object_permissions(request, note)
            note.delete()
            return ResponseHandler.success(message="Deleted", status_code=status.HTTP_204_NO_CONTENT)
        except PropertyNote.DoesNotExist:
            return ResponseHandler.error(message="Not found", status_code=status.HTTP_404_NOT_FOUND)


class SharedPropertyViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def list(self, request):
        queryset = SharedProperty.objects.filter(user=request.user)
        serializer = SharedPropertySerializer(queryset, many=True)
        return ResponseHandler.success(data=serializer.data)

    def retrieve(self, request, pk=None):
        try:
            shared = SharedProperty.objects.get(pk=pk, user=request.user)
            self.check_object_permissions(request, shared)
            serializer = SharedPropertySerializer(shared)
            return ResponseHandler.success(data=serializer.data)
        except SharedProperty.DoesNotExist:
            return ResponseHandler.error(message="Not found", status_code=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = SharedPropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return ResponseHandler.success(data=serializer.data, status_code=status.HTTP_201_CREATED)
        return ResponseHandler.error(data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
