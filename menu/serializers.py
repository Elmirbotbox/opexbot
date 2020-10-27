from rest_framework import serializers
from .models import Category, Product


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'product_image', 'ingridients',
                  'price', 'is_active', 'photo_url')

    def get_photo_url(self, obj):
        return obj.product_image.url
