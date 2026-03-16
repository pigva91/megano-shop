from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from profiles.models import Profile


class Category(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="subcategories",
    )

    def __str__(self):
        return self.title


def category_images_directory_path(
    instance: "CategoryImage", filename: str
) -> str:
    category = instance.category
    return f"catalog/categories/category_{category.pk}/{filename}"


class CategoryImage(models.Model):
    class Meta:
        verbose_name = "Изображение категорий"

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="image",
    )
    src = models.ImageField(upload_to=category_images_directory_path)
    alt = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.alt or str(self.src.name)


class Tag(models.Model):
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-date"]

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    price = models.DecimalField(max_digits=12, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    fullDescription = models.TextField(blank=True)
    freeDelivery = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title


def product_images_directory_path(
    instance: "ProductImage", filename: str
) -> str:
    product = instance.product
    return f"catalog/products/product_{product.pk}/{filename}"


class ProductImage(models.Model):
    class Meta:
        verbose_name = "Изображение товара"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        blank=True,
        null=True,
    )
    src = models.ImageField(upload_to=product_images_directory_path)
    alt = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.alt or str(self.src.name)


class Review(models.Model):
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-date"]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_reviews"
    )
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )
    email = models.EmailField()
    text = models.TextField()
    rate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=0,
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.fullName.capitalize()} - отзыв на {self.product}"


class Specification(models.Model):
    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_specifications",
    )
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return str(self.product)


class Sales(models.Model):
    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    price = models.DecimalField(max_digits=12, decimal_places=2)
    salePrice = models.DecimalField(max_digits=12, decimal_places=2)
    dateFrom = models.DateField()
    dateTo = models.DateField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_sales"
    )

    def __str__(self):
        return f"{self.product.title} - новая цена {self.salePrice}$"


class Banner(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="banners"
    )
