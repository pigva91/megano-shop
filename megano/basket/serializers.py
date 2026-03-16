from rest_framework import serializers

from catalog.serializers import (
    ProductImageSerializer,
    TagSerializer,
    ReviewSerializer,
)


class BasketItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="product.id")
    category = serializers.IntegerField(source="product.category.id")
    price = serializers.DecimalField(
        source="product.price", max_digits=12, decimal_places=2
    )
    count = serializers.IntegerField()
    date = serializers.DateTimeField(source="product.date")
    title = serializers.CharField(source="product.title")
    description = serializers.CharField(source="product.description")
    freeDelivery = serializers.BooleanField(source="product.freeDelivery")
    images = ProductImageSerializer(
        source="product.images", many=True, read_only=True
    )
    tags = TagSerializer(source="product.tags", many=True, read_only=True)
    reviews = ReviewSerializer(
        source="product.reviews", many=True, read_only=True
    )
    rating = serializers.DecimalField(
        source="product.rating", max_digits=5, decimal_places=2, read_only=True
    )


class BasketSerializer(serializers.Serializer):
    def get(self, instance):
        if isinstance(instance, list):
            return [BasketItemSerializer(item).data for item in instance]
        return super().get(instance)
