from django.db import models

from catalog.models import Product
from profiles.models import Profile


class Basket(models.Model):
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        unique_together = ["user", "product"]

    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="basket_user"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="basket_product"
    )
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} x {self.count} для {self.user}"
