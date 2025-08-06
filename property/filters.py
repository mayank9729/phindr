import django_filters as filters
from .models import Property

class PropertyFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    bedrooms = filters.NumberFilter(field_name="bedrooms")
    bathrooms = filters.NumberFilter(field_name="bathrooms")
    is_pet_friendly = filters.BooleanFilter()
    has_parking = filters.BooleanFilter()
    utilities_included = filters.BooleanFilter()

    class Meta:
        model = Property
        fields = ['min_price', 'max_price', 'bedrooms', 'bathrooms', 'is_pet_friendly', 'has_parking', 'utilities_included']
        
