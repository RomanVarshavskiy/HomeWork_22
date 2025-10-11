from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    """Форма создания/редактирования статьи.

    Включает основные поля модели BlogPost и кастомные виджеты
    для удобного ввода текста, чисел, дат и загрузки файлов.
    """

    class Meta:
        """Конфигурация формы BlogPost.

        Атрибуты:
            model: Модель, на основе которой строится форма.
            fields: Поля модели, отображаемые в форме.
            widgets: Кастомные виджеты для рендеринга элементов ввода.
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
