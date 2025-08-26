from django.db import models
from django.conf import settings
from customer.models import User

class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    amenities = models.ManyToManyField(Amenity, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=255)
    is_pet_friendly = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    utilities_included = models.BooleanField(default=False)
    available_from = models.DateField()
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

class SavedSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.JSONField()  

class ViewingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

class PropertyNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE,null=True, blank=True)
    note = models.TextField()
    personal_rating = models.FloatField(null=True, blank=True)


class SharedProperty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_by')
    co_applicant_email = models.EmailField()
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.co_applicant_email
    