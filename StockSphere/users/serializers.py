from rest_framework import serializers
from .models import Resource

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = [
            'id', 'name', 'price_per_pack', 'units_per_pack', 
            'unit_price', 'available_units', 'arriving_units', 'notes', 'created_at'
        ]