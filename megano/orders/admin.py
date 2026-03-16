from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("product", "count", "get_product_price", "get_subtotal")
    can_delete = False
    max_num = 0

    @admin.display(description="Цена за шт.")
    def get_product_price(self, obj: OrderItem) -> str:
        if obj.product:
            return f"{obj.product.price:,.2f} ₽"
        return "-"

    @admin.display(description="Сумма позиции")
    def get_subtotal(self, obj: OrderItem) -> str:
        if obj.product:
            return f"{obj.product.price * obj.count:,.2f} ₽"
        return "-"


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "full_name",
        "created_at",
        "city",
        "delivery_type",
        "payment_type",
    )
    list_display_links = ("pk", "full_name")
    search_fields = ("pk", "full_name", "city")
    ordering = ("pk",)
    readonly_fields = ("user", "created_at", "delivery_type", "payment_type")
    inlines = (OrderItemInline,)
    list_per_page = 20

    fieldsets = (
        (
            "Основная информация",
            {"fields": ("created_at", "user", "full_name", "email", "phone")},
        ),
        (
            "Доставка",
            {
                "fields": ("city", "address", "delivery_type"),
                "classes": ("collapse",),
            },
        ),
        (
            "Оплата и статус",
            {
                "fields": ("payment_type", "total_cost"),
                "classes": ("collapse",),
            },
        ),
    )
