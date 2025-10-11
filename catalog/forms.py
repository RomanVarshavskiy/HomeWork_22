"""Формы Django для работы с сущностями каталога.

Содержит формы:
- ProductForm: создание/редактирование товаров.
- CategoryForm: создание/редактирование категорий.

Обе формы имеют преднастроенные виджеты для удобного ввода данных в админке/шаблонах.
"""


from django import forms
from django.core.exceptions import ValidationError

from .models import Product, Category


FORBIDDEN_WORDS = (
    'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
    'бесплатно', 'обман', 'полиция', 'радар', 'spam'
)

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
        exclude = ["views_counter"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Название"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Описание"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "1.00"}),
            "created_at": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "updated_at": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name').lower()
        for word in FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError(f'Наименование товара не может содержать запрещенное слово "{word}"')
        return self.cleaned_data.get('name')

    def clean_description(self):
        description = self.cleaned_data.get('description').lower()
        for word in FORBIDDEN_WORDS:
            if word in description:
                raise ValidationError(f'Описание товара не может содержать запрещенное слово "{word}"')
        return self.cleaned_data.get('description')

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Цена товара не может быть отрицательной')
        return price



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