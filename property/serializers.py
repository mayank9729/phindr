from rest_framework import serializers
from .models import *

class AmenitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Amenity
        fields = '__all__'

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError({"message":"Amenity name cannot be empty."})
        return value

class PropertySerializer(serializers.ModelSerializer):
    #property = serializers.StringRelatedField(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    class Meta:
        model = Property
        fields = '__all__'

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError({"message":"Price must be a positive number."})
        return value

class FavoriteSerializer(serializers.ModelSerializer):
    property=PropertySerializer(read_only=True)
    user= serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Favorite
        fields = '__all__'

class SavedSearchSerializer(serializers.ModelSerializer):
    property=PropertySerializer(read_only=True)
    user= serializers.StringRelatedField(read_only=True)
    class Meta:
        model = SavedSearch
        fields = '__all__'

class ViewingHistorySerializer(serializers.ModelSerializer):
    #property = serializers.StringRelatedField(read_only=True)
    user= serializers.StringRelatedField(read_only=True)
    property=PropertySerializer(read_only=True)
    class Meta:
        model = ViewingHistory
        fields = '__all__'

class PropertyNoteSerializer(serializers.ModelSerializer):
  #  property = serializers.StringRelatedField(read_only=True)
    user= serializers.StringRelatedField(read_only=True)
    property=PropertySerializer(read_only=True)
    class Meta:
        model = PropertyNote
        fields = '__all__'

class SharedPropertySerializer(serializers.ModelSerializer):
   # property = serializers.StringRelatedField(read_only=True)
    user= serializers.StringRelatedField(read_only=True)
    property=PropertySerializer(read_only=True)
    class Meta:
        model = SharedProperty
        fields = '__all__'
