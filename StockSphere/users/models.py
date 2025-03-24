from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)

class Resource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resources')
    name = models.CharField(max_length=255)
    price_per_pack = models.DecimalField(max_digits=10, decimal_places=2)  # Price per pack
    units_per_pack = models.PositiveIntegerField()  # Number of units in a pack
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Auto-calculated
    available_units = models.PositiveIntegerField()  # How many units are in stock
    arriving_units = models.PositiveIntegerField(blank=True, null=True)  # Expected arrival of units
    notes = models.TextField(blank=True, null=True)  # Additional notes
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """ Auto calculate unit_price based on price_per_pack and unit_per_pack. """
        if self.units_per_pack > 0 :
            self.unit_price = self.price_per_pack / self.units_per_pack
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name