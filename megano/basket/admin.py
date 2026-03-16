from django.contrib import admin

from .models import Basket


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "product", "count", "total_price")
    list_display_links = ("pk", "user")
    search_fields = ("pk", "product__title")
    readonly_fields = ("user", "product", "count")

    @admin.display(description="Сумма позиции")
    def total_price(self, obj):
        return f"{obj.product.price * obj.count:,.2f} ₽"
