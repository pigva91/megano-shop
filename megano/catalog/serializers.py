from datetime import timezone

from rest_framework import serializers

from .models import (
    Category,
    CategoryImage,
    Product,
    ProductImage,
    Review,
    Sales,
    Specification,
    Tag,
)


class ProductImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()
    alt = serializers.CharField()

    class Meta:
        model = ProductImage
        fields = ["src", "alt"]

    def get_src(self, obj):
        if obj.src:
            return obj.src.url
        return ""


class CatalogImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()
    alt = serializers.CharField()

    class Meta:
        model = CategoryImage
        fields = ["src", "alt"]

    def get_src(self, obj):
        if obj.src:
            return obj.src.url
        return ""


class SubCategorySerializer(serializers.ModelSerializer):
    image = CatalogImageSerializer(source="image.first")

    class Meta:
        model = Category
        fields = ["id", "title", "image"]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True)
    image = CatalogImageSerializer(source="image.first")

    class Meta:
        model = Category
        fields = ["id", "title", "image", "subcategories"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.fullName", read_only=True)
    date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M", default_timezone=timezone.utc, read_only=True
    )

    class Meta:
        model = Review
        fields = ("author", "email", "text", "rate", "date")


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ("name", "value")


class SaleItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="product.id")
    title = serializers.CharField(source="product.title")
    images = ProductImageSerializer(many=True, source="product.images")
    dateFrom = serializers.DateField(format="%m-%d")
    dateTo = serializers.DateField(format="%m-%d")

    class Meta:
        model = Sales
        fields = (
            "id",
            "price",
            "salePrice",
            "dateFrom",
            "dateTo",
            "title",
            "images",
        )


class ProductShortSerializer(serializers.ModelSerializer):
    category = serializers.IntegerField(source="category.id")
    images = ProductImageSerializer(many=True)
    tags = TagSerializer(many=True)
    date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", default_timezone=timezone.utc
    )
    reviews = ReviewSerializer(many=True, source="product_reviews")

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        )


class ProductSerializer(ProductShortSerializer):
    specifications = SpecificationSerializer(
        many=True, source="product_specifications"
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        )
