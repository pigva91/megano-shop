from django.db import models

from orders.models import Order


class Payment(models.Model):
    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платёжи"

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Заказ",
    )
    number = models.CharField(max_length=16, verbose_name="Номер карты")
    name = models.CharField(max_length=100, verbose_name="Имя держателя карты")
    month = models.CharField(max_length=2, verbose_name="Месяц")
    year = models.CharField(max_length=2, verbose_name="Год")
    code = models.CharField(max_length=3, verbose_name="CVV код")

    def __str__(self) -> str:
        return f"Платёж по заказу № {self.order_id} - {self.name}"
