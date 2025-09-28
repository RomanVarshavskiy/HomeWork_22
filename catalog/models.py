from django.db import models


class Product(models.Model):
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
        verbose_name="Дата создания", help_text="Укажите дату создания", null=True, blank=True
    )
    updated_at = models.DateField(
        verbose_name="Дата последнего изменения", help_text="Укажите дату последнего изменения", null=True, blank=True
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name", "category", "price", "updated_at"]

    def __str__(self):
        return f"{self.category}: {self.name}"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование", help_text="Введите наименование категории")
    description = models.TextField(
        verbose_name="Описание", help_text="Укажите описание категории", null=True, blank=True
    )
    image = models.ImageField(
        upload_to="catalog/image", verbose_name="Изображение", help_text="Загрузите изображение", null=True, blank=True
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя", help_text="Введите имя")
    phone = models.CharField("Телефон", max_length=32)
    email = models.EmailField("Email", blank=True, null=True)
    address = models.CharField("Адрес", max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f"{self.name}:    {self.phone},  {self.email}"
