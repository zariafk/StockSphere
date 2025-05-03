from rest_framework import serializers
from .models import Resource, Product, Delivery, DeliveryResource, Post, Community, Comment

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
    
    def validate_sales_forecast(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("sales_forecast must be a list.")
        for forecast in value:
            if 'platform' not in forecast or 'periods' not in forecast:
                raise serializers.ValidationError("Each forecast must include 'platform' and 'periods'.")
            for period in forecast['periods']:
                if 'unitsSold' not in period:
                    raise serializers.ValidationError("Each period must include 'unitsSold'.")
            # Optional: warn or enforce dates
                if 'startDate' not in period or 'endDate' not in period:
                    raise serializers.ValidationError("Each period must include 'startDate' and 'endDate'.")
        return value



class DeliveryResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryResource
        fields = ['id', 'resource', 'cases']

class DeliverySerializer(serializers.ModelSerializer):
    resources = DeliveryResourceSerializer(many=True)

    class Meta:
        model = Delivery
        fields = ['id', 'from_location', 'notes', 'completed', 'created_at', 'resources']

    def create(self, validated_data):
        resources_data = validated_data.pop('resources')
        delivery = Delivery.objects.create(**validated_data)
        for resource_data in resources_data:
            DeliveryResource.objects.create(delivery=delivery, **resource_data)
        return delivery

def update(self, instance, validated_data):
    resources_data = validated_data.pop('resources', None)

    instance.from_location = validated_data.get('from_location', instance.from_location)
    instance.notes = validated_data.get('notes', instance.notes)
    instance.completed = validated_data.get('completed', instance.completed)
    instance.save()

    # 🛠 Only update resources if new ones were actually provided
    if resources_data is not None:
        instance.resources.all().delete()
        for resource_data in resources_data:
            DeliveryResource.objects.create(delivery=instance, **resource_data)

    return instance


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'name', 'description']

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'author_username']

class PostSerializer(serializers.ModelSerializer):
    from .serializers import CommentSerializer
    community = serializers.PrimaryKeyRelatedField(queryset=Community.objects.all())  # Expect Community ID
    comments = CommentSerializer(many=True, read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'community', 'author', 'created_at', 'comments', 'author_username']
