from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок", help_text="Введите название заголовка статьи")
    content = models.TextField(verbose_name="Содержимое", help_text="Укажите содержимое статьи", null=True, blank=True)
    preview_image = models.ImageField(
        upload_to="myblog/image", verbose_name="Превью (изображение)", help_text="Загрузите изображение", null=True,
        blank=True
    )
    created_at = models.DateField(
        verbose_name="Дата создания", help_text="Укажите дату создания", null=True, blank=True
    )
    updated_at = models.DateField(
        verbose_name="Дата последнего изменения", help_text="Укажите дату последнего изменения", null=True, blank=True
    )
    is_published = models.BooleanField(default=False)

    views_counter = models.PositiveIntegerField(default=0, verbose_name="Счетчик просмотров",
                                                help_text="Укажите количество просмотров")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["title", "created_at", "views_counter"]

    def __str__(self):
        return {self.title}
