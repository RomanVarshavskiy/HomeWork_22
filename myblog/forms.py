from django import forms
from django.core.exceptions import ValidationError

from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    """Форма для создания и редактирования статей блога.

    Использует модель BlogPost, скрывает служебные поля и настраивает виджеты
    для удобного ввода данных в админке/шаблонах.
    """

    class Meta:
        """Метаданные формы BlogPostForm.

        Атрибуты:
            model: Связанная модель (BlogPost).
            exclude: Поля, исключённые из формы (например, счётчик просмотров).
            widgets: Кастомные виджеты для полей формы (классы, плейсхолдеры, типы полей).
        """

        model = BlogPost
        exclude = ("views_counter",)
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Заголовок"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Содержимое"}),
            "preview_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "created_at": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "updated_at": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def clean_image(self):
        """Валидация поля изображения.

        Проверяет:
        - отсутствие значения (возвращает как есть, если файл не загружен);
        - максимальный размер файла (до 5 МБ);
        - MIME-тип (только image/jpeg или image/png);
        - расширение имени файла (.jpg, .jpeg, .png).
        """

        image = self.cleaned_data.get("image")
        if not image:
            return image
        max_size = 5 * 1024 * 1024  # 5 MB
        if hasattr(image, "size") and image.size > max_size:
            raise ValidationError("Размер файла не должен превышать 5 МБ.")

        content_type = getattr(image, "content_type", "")
        allowed_types = {"image/jpeg", "image/png"}
        if content_type not in allowed_types:
            raise ValidationError("Допустимы только изображения в формате JPEG или PNG.")

        name = getattr(image, "name", "") or ""
        if not name.lower().endswith((".jpg", ".jpeg", ".png")):
            raise ValidationError("Файл должен иметь расширение .jpg, .jpeg или .png.")
