from django.contrib import admin
from django.utils.html import format_html

from catalog.models import (
    Category,
    CategoryImage,
    ProductImage,
    Product,
    Review,
    Sales,
    Specification,
    Tag,
)


class CategoryImageInline(admin.StackedInline):
    model = CategoryImage
    max_num = 1
    fields = ("src", "alt", "image_preview")
    readonly_fields = ("image_preview",)

    @admin.display(description="Превью")
    def image_preview(self, obj):
        if obj.src:
            return format_html(
                "<img src='{}' style='max-height: 50px;'/>", obj.src.url
            )
        return "-"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "parent")
    list_display_links = ("pk", "title")
    search_fields = ("title",)
    inlines = (CategoryImageInline,)
    ordering = ("pk",)


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1
    fields = ("src", "alt", "image_preview")
    readonly_fields = ("image_preview",)

    @admin.display(description="Превью")
    def image_preview(self, obj):
        if obj.src:
            return format_html(
                "<img src='{}' style='max-height: 50px;'/>", obj.src.url
            )
        return "-"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "price",
        "category",
        "count",
        "date",
        "freeDelivery",
        "rating",
    )
    list_display_links = ("pk", "title")
    search_fields = ("title", "price")
    inlines = (ProductImageInline,)
    ordering = ("date", "pk")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "product", "author_str", "rate", "date")
    list_display_links = ("pk", "product")
    search_fields = ("author__fullName", "product__title")
    ordering = ("-date", "pk")
    readonly_fields = ("product", "date", "author_str")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "product",
                    "author_str",
                    "email",
                    "text",
                    "rate",
                    "date",
                )
            },
        ),
    )

    @admin.display(description="Автор", ordering="author__fullName")
    def author_str(self, obj):
        if not obj.author:
            return "-"
        return obj.author.fullName.capitalize()

    def get_queryset(self, request):
        return (
            super().get_queryset(request).select_related("author", "product")
        )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    list_display_links = ("pk", "name")
    search_fields = ("pk", "name")
    ordering = ("pk", "name")


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ("pk", "product")
    list_display_links = ("pk", "product")
    search_fields = ("pk", "product__title")
    ordering = ("pk", "name")


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "product",
        "price",
        "salePrice",
        "discount",
        "dateFrom",
        "dateTo",
    )
    list_display_links = ("pk", "product")
    search_fields = ("product__title",)
    ordering = ("pk", "product")

    @admin.display(description="Скидка")
    def discount(self, obj):
        if obj.price and obj.salePrice:
            disc = (obj.price - obj.salePrice) / obj.price * 100
            return f"{disc:.0f}%"
        return "-"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")
