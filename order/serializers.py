from rest_framework import serializers
from order.models import Client, OrderItem, BasketList, FavoriteList
from menu.serializers import ProductSerializer


class ClientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            'client_id',
            'product',
            'quantity',
            'final_price',
            'owner',
        )

    def get_product(self, obj, request):
        return ProductSerializer(obj.product,  context={"request": request}).data

    def get_final_price(self, obj):
        return obj.get_final_price()


class FavoriteListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = FavoriteList
        fields = (
            'client_id',
            'product',
            'owner'
        )

    def get_product(self, obj, request):
        return ProductSerializer(obj.product, context={"request": request}).data


class BasketListSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = BasketList
        fields = (
            'id',
            'daily_id',
            'client_id',
            'time',
            'items',
            'owner',
            'status',
            'total',
            'comment',
            'deliveryType',
            'paymentType'
        )

    def get_total(self, obj):
        return obj.get_total()

    def get_items(self, obj):
        return OrderItemSerializer(obj.items.all(), many=True).data
