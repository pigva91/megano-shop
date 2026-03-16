from rest_framework import serializers

from basket.serializers import BasketItemSerializer
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    products = BasketItemSerializer(source="items", many=True, read_only=True)
    createdAt = serializers.DateTimeField(
        source="created_at", format="%Y-%m-%d %H:%M"
    )
    fullName = serializers.CharField(source="full_name")
    deliveryType = serializers.CharField(source="delivery_type")
    paymentType = serializers.CharField(source="payment_type")
    totalCost = serializers.DecimalField(
        source="total_cost", max_digits=12, decimal_places=2
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        ]


class OrderCreateSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100, allow_blank=True)
    address = serializers.CharField(allow_blank=True)
    deliveryType = serializers.CharField()
    paymentType = serializers.CharField()


class OrderIdResponseSerializer(serializers.Serializer):
    orderId = serializers.IntegerField(source="id")
