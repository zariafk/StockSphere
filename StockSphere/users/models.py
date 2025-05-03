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
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    cost = models.FloatField()
    sales_price = models.FloatField()
    profit = models.FloatField()
    units_in_stock = models.IntegerField()
    notes = models.TextField(null=True, blank=True)
    sales_forecast = models.JSONField(default=list)
    resource_usages = models.JSONField(default=list)  # Store the resource usage as JSON
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Each product is linked to a user

    def __str__(self):
        return self.name
    
class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message}"

    
class Delivery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_location = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery from {self.from_location} on {self.created_at.strftime('%Y-%m-%d')}"

class DeliveryResource(models.Model):
    delivery = models.ForeignKey(Delivery, related_name='resources', on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    cases = models.PositiveIntegerField()

    def total_units(self):
        return self.cases * self.resource.units_per_pack

    def total_cost(self):
        return self.total_units() * self.resource.unit_price

    def __str__(self):
        return f"{self.cases}x {self.resource.name} in {self.delivery}"
    
class Community(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Post(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='Default Title')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

