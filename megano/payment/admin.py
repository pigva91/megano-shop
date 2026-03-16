from django.contrib import admin
from rest_framework.request import Request

from payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "masked_number",
    )
    list_display_links = ("pk", "name")
    search_fields = ("pk", "name")
    ordering = ("pk",)
    list_per_page = 20
    readonly_fields = ("order",)
    fields = ("order", "name", "number", "month", "year")

    @admin.display(description="Номер карты")
    def masked_number(self, obj: Payment) -> str:
        if obj.number and len(obj.number) == 16:
            return f"{obj.number[:4]}{'*' * (len(obj.number) - 4)}"
        return "-"

    def has_add_permission(self, request: Request) -> bool:
        return False

    def has_delete_permission(self, request: Request, obj=None) -> bool:
        return False
