from rest_framework import serializers
from apps.catalog.models import Category, Item


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        read_only_fields = '__all__'

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk','slug',)

class ItemSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    class Meta:
        model = Item
        read_only_fields = '__all__'

class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('pk','name',)       