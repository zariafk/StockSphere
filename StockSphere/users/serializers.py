from rest_framework import serializers
from .models import Resource, Product

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = [
            'id', 'name', 'price_per_pack', 'units_per_pack', 
            'unit_price', 'available_units', 'arriving_units', 'notes', 'created_at'
        ]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False}  # <- Make 'user' not required
        }

    def validate_resource_usages(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("resource_usages must be a list.")
        for item in value:
            if not isinstance(item, dict):
                raise serializers.ValidationError("Each resource usage must be a dictionary.")
            if 'resourceId' not in item or 'units' not in item:
                raise serializers.ValidationError("Each resource usage must have 'resourceId' and 'units'.")
            if not isinstance(item['units'], (int, float)) or item['units'] <= 0:
                raise serializers.ValidationError("'units' must be a positive number.")
        return value
