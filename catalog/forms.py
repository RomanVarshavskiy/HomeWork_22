"""Формы Django для работы с сущностями каталога.

Содержит формы:
- ProductForm: создание/редактирование товаров.
- CategoryForm: создание/редактирование категорий.

Обе формы имеют преднастроенные виджеты для удобного ввода данных в админке/шаблонах.
"""


from django import forms

from .models import Product, Category


class ProductForm(forms.ModelForm):
    """Форма создания/редактирования товара.

    Включает основные поля модели Product и кастомные виджеты
    для удобного ввода текста, чисел, дат и загрузки файлов.
    """

    class Meta:
        """Конфигурация формы ProductForm.

        Атрибуты:
            model: Модель, на основе которой строится форма.
            fields: Поля модели, отображаемые в форме.
            widgets: Кастомные виджеты для рендеринга элементов ввода.
        """
        model = Product
        fields = ["name", "description", "image", "category", "price", "created_at", "updated_at"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Название"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Описание"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "created_at": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "updated_at": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

class CategoryForm(forms.ModelForm):
    """Форма создания/редактирования категории.

    Предоставляет поля и виджеты для ввода названия, описания и загрузки изображения категории.
    """

    class Meta:
        """Конфигурация формы CategoryForm.

        Атрибуты:
            model: Модель, используемая для построения формы.
            fields: Список полей, включённых в форму.
            widgets: Виджеты для настройки внешнего вида и поведения полей.
        """

        model = Category
        fields = ["name", "description", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Название"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Описание"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }