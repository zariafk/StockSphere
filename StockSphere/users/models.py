from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    price_per_pack = models.DecimalField(max_digits=10, decimal_places=2)  # Price per pack
    units_per_pack = models.PositiveIntegerField()  # Number of units in a pack
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Auto-calculated
    available_units = models.PositiveIntegerField()  # How many units are in stock
    arriving_units = models.PositiveIntegerField()  # Expected arrival of units
    notes = models.TextField(blank=True, null=True)  # Additional notes
    created_at = models.DateTimeField(auto_now_add=True)