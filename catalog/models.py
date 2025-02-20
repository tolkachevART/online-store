from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование категории")
    description = models.TextField(verbose_name="Описание категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование товара")
    description = models.TextField(verbose_name="Описание товара")
    image = models.ImageField(
        upload_to="product/img", verbose_name="Превью товара", **NULLABLE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        **NULLABLE,
        related_name="products"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за покупку"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        **NULLABLE,
        related_name="products",
    )
    is_published = models.BooleanField(
        default=False, verbose_name="Опубликованные товары")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name", "category"]
        permissions = [
            ("can_edit_category", "Can edit any category"),
            ("can_edit_description", "Can edit any description"),
            ("can_unpublish_product", "Can unpublish of a product")
        ]


class Version(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="versions", verbose_name="Товар"
    )
    version_number = models.CharField(max_length=20, verbose_name="Номер версии")
    version_name = models.CharField(max_length=100, verbose_name="Название версии")
    is_current = models.BooleanField(default=False, verbose_name="Текущая версия")

    def __str__(self):
        return f"{self.product.name} - {self.version_name}"

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = ["is_current", "version_number"]
        unique_together = ["product", "version_number"]
