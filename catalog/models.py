"""Модели приложения каталога."""

from django.db import models


class Product(models.Model):
    """Товар каталога."""

    name = models.CharField(max_length=100, verbose_name="Наименование", help_text="Введите наименование товара")
    description = models.TextField(verbose_name="Описание", help_text="Укажите описание товара", null=True, blank=True)
    image = models.ImageField(
        upload_to="catalog/image", verbose_name="Изображение", help_text="Загрузите изображение", null=True, blank=True
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория",
        help_text="Введите категорию товара",
        related_name="products",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за покупку", help_text="Укажите цену"
    )
    created_at = models.DateField(
        verbose_name="Дата создания", help_text="Укажите дату создания", null=True, blank=True#, auto_now_add=True
    )
    updated_at = models.DateField(
        verbose_name="Дата последнего изменения", help_text="Укажите дату последнего изменения", null=True, blank=True#, auto_now=True
    )

    views_counter = models.PositiveIntegerField(default=0, verbose_name="Счетчик просмотров",
                                                help_text="Укажите количество просмотров")

    class Meta:
        """Метаданные модели Product.

        Атрибуты:
            verbose_name: Человекочитаемое имя модели в единственном числе.
            verbose_name_plural: Имя во множественном числе.
            ordering: Порядок сортировки по умолчанию.
        """

        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name", "category", "price", "updated_at"]

    def __str__(self):
        """Строковое представление товара: '<Категория>: <Наименование>'."""
        return f"{self.category}: {self.name}"


class Category(models.Model):
    """Категория товаров."""

    name = models.CharField(max_length=100, verbose_name="Наименование", help_text="Введите наименование категории")
    description = models.TextField(
        verbose_name="Описание", help_text="Укажите описание категории", null=True, blank=True
    )
    image = models.ImageField(
        upload_to="catalog/image", verbose_name="Изображение", help_text="Загрузите изображение", null=True, blank=True
    )

    class Meta:
        """Метаданные модели Category."""
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        """Строковое представление категории: её наименование."""
        return self.name


class Contact(models.Model):
    """Контактная запись."""

    name = models.CharField(max_length=150, verbose_name="Имя", help_text="Введите имя")
    phone = models.CharField("Телефон", max_length=32)
    email = models.EmailField("Email", blank=True, null=True)
    address = models.CharField("Адрес", max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        """Метаданные модели Contact."""
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        """Строковое представление контакта: '<Имя>: <телефон>, <email>'."""
        return f"{self.name}:    {self.phone},  {self.email}"
