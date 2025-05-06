from django.contrib.auth.models import User
from django.db import models

# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)

# Resource model
class Resource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resources') # Resource belongs to a user
    name = models.CharField(max_length=255)
    price_per_pack = models.DecimalField(max_digits=10, decimal_places=2)  
    units_per_pack = models.PositiveIntegerField()  
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Auto-calculated
    available_units = models.PositiveIntegerField()  
    arriving_units = models.PositiveIntegerField(blank=True, null=True)  
    notes = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto calculate unit_price based on price_per_pack and unit_per_pack.
        if self.units_per_pack > 0 :
            self.unit_price = self.price_per_pack / self.units_per_pack
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name    #Display resource name when printed
    
# Product model
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
        return self.name # Return product name when printed
    
# Notification model that stores notifications for users
class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message}"

# Delivery model
class Delivery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Delivery belongs to a user
    from_location = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery from {self.from_location} on {self.created_at.strftime('%Y-%m-%d')}"

# DeliveryResource model that links resources to deliveries
class DeliveryResource(models.Model):
    delivery = models.ForeignKey(Delivery, related_name='resources', on_delete=models.CASCADE) # Link to delivery
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE) # Link to resource
    cases = models.PositiveIntegerField()

    # Calculate total units of resource in delivery
    def total_units(self):
        return self.cases * self.resource.units_per_pack

    # Calculate total cost of resource in delivery
    def total_cost(self):
        return self.total_units() * self.resource.unit_price

    def __str__(self):
        return f"{self.cases}x {self.resource.name} in {self.delivery}"

# Community model
class Community(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE) # User who created the community

# Post model for storing posts within a community
class Post(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE) # Each post belongs to a community
    author = models.ForeignKey(User, on_delete=models.CASCADE) # Each post was made by an author, i.e. user
    title = models.CharField(max_length=255, default='Default Title')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp of when post was created

    def __str__(self):
        return self.title

# Comment model 
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) # Each comment belongs to a post
    author = models.ForeignKey(User, on_delete=models.CASCADE) # Each comment has an author, i.e. user
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp of when comment was created 

    def __str__(self):
        return self.content