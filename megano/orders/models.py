from django.core.validators import MinValueValidator
from django.db import models

from catalog.models import Product
from profiles.models import Profile


class Order(models.Model):
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    user = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="orders",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=12, verbose_name="Телефон")
    delivery_type = models.CharField(
        max_length=50, verbose_name="Тип доставки"
    )
    payment_type = models.CharField(max_length=50, verbose_name="Тип оплаты")
    total_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Общая сумма",
    )
    status = models.CharField(max_length=50, verbose_name="Статус")
    city = models.CharField(max_length=100, verbose_name="Город")
    address = models.TextField(verbose_name="Адрес доставки")

    def __str__(self) -> str:
        return f"Заказ №{self.pk} - {self.full_name or 'Гость'}"


class OrderItem(models.Model):
    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Заказ",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Товар",
    )
    count = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self) -> str:
        return f"{self.product.title}"
