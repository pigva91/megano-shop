from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Модель профиля пользователя."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    fullName = models.CharField(
        null=True, blank=True, max_length=128, verbose_name="Полное имя"
    )
    email = models.EmailField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
    )
    phone = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        unique=True,
        verbose_name="Номер телефона",
    )
    avatar = models.ForeignKey(
        "Avatar",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Аватар",
    )


class Avatar(models.Model):
    """Модель для хранения аватара пользователя."""

    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватары"

    src = models.ImageField(
        default="default.png",
        verbose_name="Ссылка",
    )
    alt = models.CharField(max_length=128, verbose_name="Описание")
