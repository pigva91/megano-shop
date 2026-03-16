from datetime import date

from django.db.models import Count, Avg
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Tag, Product, Sales
from .pagination import CatalogPagination
from .serializers import (
    CategorySerializer,
    TagSerializer,
    ProductSerializer,
    ProductShortSerializer,
    ReviewSerializer,
    SaleItemSerializer,
)


class CategoriesAPIView(APIView):
    def get(self, request):
        categories = Category.objects.filter(parent=None).prefetch_related(
            "subcategories"
        )
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CatalogListAPIView(ListAPIView):
    pagination_class = CatalogPagination
    serializer_class = ProductShortSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["rating", "price", "date"]

    def get_queryset(self):
        queryset = (
            Product.objects.all()
            .select_related("category")
            .prefetch_related("images", "tags")
            .annotate(review_count=Count("product_reviews"))
        )

        params = self.request.query_params
        if category_id := params.get("category"):
            try:
                Category.objects.get(id=category_id)
                subcategory_ids = Category.objects.filter(
                    parent_id=category_id
                ).values_list("pk", flat=True)
                queryset = queryset.filter(
                    category_id__in=[category_id] + list(subcategory_ids)
                )
            except Category.DoesNotExist:
                return Product.objects.none()

        if name := params.get("filter[name]"):
            queryset = queryset.filter(title__icontains=name)

        if min_price := params.get("filter[minPrice]"):
            queryset = queryset.filter(price__gte=float(min_price))

        if max_price := params.get("filter[maxPrice]"):
            queryset = queryset.filter(price__lte=float(max_price))

        if params.get("filter[freeDelivery]") == "true":
            queryset = queryset.filter(freeDelivery=True)

        if params.get("filter[available]") == "true":
            queryset = queryset.filter(count__gt=0)

        if tag_ids := params.getlist("tags"):
            queryset = queryset.filter(tags__id__in=tag_ids).distinct()

        sort = params.get("sort", "date")
        sort_type = params.get("sortType", "dec")
        sort_field_map = {
            "rating": "rating",
            "price": "price",
            "reviews": "review_count",
            "date": "date",
        }
        sort_field = sort_field_map.get(sort, "date")

        if sort_type == "inc":
            queryset = queryset.order_by(sort_field)
        else:
            queryset = queryset.order_by(f"-{sort_field}")

        return queryset


class ProductsPopularAPIView(APIView):
    def get(self, request):
        products = Product.objects.order_by("-count")[:8]
        serializer = ProductShortSerializer(products, many=True)
        return Response(serializer.data)


class ProductsLimitedAPIView(APIView):
    def get(self, request):
        today = date.today()
        products = Product.objects.filter(
            product_sales__dateFrom__lte=today,
            product_sales__dateTo__gte=today,
        )[:16]
        serializer = ProductShortSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailsAPIView(APIView):
    def get(self, request, id):
        product = (
            Product.objects.select_related("category")
            .prefetch_related(
                "images", "tags", "product_reviews", "product_specifications"
            )
            .get(id=id)
        )
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class ReviewCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        product = Product.objects.get(pk=id)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                product=product,
                author=request.user.profile,
                email=request.user.profile.email,
            )
            reviews_qs = product.product_reviews.all()

            if reviews_qs.exists():
                avg = reviews_qs.aggregate(avg=Avg("rate"))["avg"] or 0
                product.rating = round(avg, 2)
            else:
                product.rating = 0.00
            product.save()

            all_reviews = ReviewSerializer(
                reviews_qs.order_by("-date"), many=True
            )
            return Response(all_reviews.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagsAPIView(APIView):
    def get(self, request):
        category_id = request.query_params.get("category")
        if category_id:
            Category.objects.get(pk=category_id)
            subcategory_ids = Category.objects.filter(
                parent_id=category_id
            ).values_list("id", flat=True)
            category_ids = [category_id] + list(subcategory_ids)
            tags = Tag.objects.filter(
                product__category_id__in=category_ids
            ).distinct()
        else:
            tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


class SalesListAPIView(ListAPIView):
    queryset = Sales.objects.select_related("product").order_by("-dateTo")
    serializer_class = SaleItemSerializer
    pagination_class = CatalogPagination


class BannersAPIView(APIView):
    def get(self, request):
        products = Product.objects.order_by("-date")[:3]
        serializer = ProductShortSerializer(products, many=True)
        return Response(serializer.data)
