"""Представления (CBV/FBV) для приложения каталога.

Содержит CRUD-представления для моделей Product и Category, страницу контактов
с простой обработкой формы и главную страницу с выборкой последних товаров.
"""


from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views import View

from catalog.forms import ProductForm, CategoryForm
from catalog.models import Contact, Product, Category


class ProductCreateView(CreateView):
    """Создание товара.

    Атрибуты:
        model: Модель товара.
        fields: Поля, доступные для ввода.
        template_name: Шаблон формы создания.
        success_url: URL редиректа после успешного создания.
    """

    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products_list')


class ProductListView(ListView):
    """Список товаров.

    Атрибуты:
        model: Модель товара.
        template_name: Шаблон списка.
        context_object_name: Имя переменной контекста для списка товаров.
    """

    model = Product
    template_name = 'catalog/products_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    """Детальная страница товара.

    Дополнительно:
        - Инкрементирует счётчик просмотров при каждом запросе.
    """

    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        """Возвращает объект товара и увеличивает счётчик просмотров.

        Параметры:
            queryset: Необязательный QuerySet для выборки объекта.
        Возврат:
            Product: Объект товара с обновлённым счётчиком просмотров.
        """
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProductUpdateView(UpdateView):
    """Редактирование товара.

    Атрибуты:
        model: Модель товара.
        fields: Поля, доступные для редактирования.
        template_name: Шаблон формы.
        success_url: URL по умолчанию (может быть переопределён методом get_success_url()).
    """

    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products_list')

    def get_success_url(self):
        """URL для редиректа после успешного обновления.
        Ведёт на страницу детали товара.
        """
        return reverse_lazy('catalog:product_detail', args={self.kwargs.get('pk')})


class ProductDeleteView(DeleteView):
    """Удаление товара.

    Атрибуты:
        model: Модель товара.
        template_name: Шаблон подтверждения удаления.
        success_url: URL редиректа к списку товаров после удаления.
    """

    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:products_list')


def home(request):
    """Главная страница каталога.

    Действия:
        - Получает все товары.
        - Формирует список последних 5 товаров по полю created_at.
        - Передаёт оба набора данных в шаблон 'catalog/home.html'.
    Параметры:
        request (HttpRequest): Объект запроса.
    Возврат:
        HttpResponse: Сформированный ответ с отрендеренным шаблоном.
    """

    # Получаем все продукты
    products = Product.objects.all()

    # Берём последние 5 продуктов по полю created_at
    last_products = products.order_by("-created_at")[:5]

    # Выводим данные в консоль сервера (терминал, где запущен runserver)
    print("Последние 5 продуктов:")
    for p in last_products:
        print(f"- [{p.id}] {p.name} | создан: {p.created_at} | цена: {p.price}")

    # Передаём оба queryset'а в шаблон
    return render(request, "catalog/home.html", {
        "products": products,
        "last_products": last_products,
    })


class ContactsView(ListView):
    """Страница контактов с обработкой формы.

    Атрибуты:
        model: Модель Contact для отображения контактных записей.
        template_name: Шаблон страницы контактов.
        context_object_name: Имя переменной контекста со списком контактов.
    """

    model = Contact
    template_name = "catalog/contacts.html"
    context_object_name = "contacts"

    def post(self, request, *args, **kwargs):
        """Обрабатывает отправку формы с контактным сообщением.

        Ожидаемые поля формы:
            name (str): Имя отправителя.
            phone (str): Телефон.
            message (str): Текст сообщения.
        Возврат:
            HttpResponse: Короткий ответ-подтверждение успешной отправки.
        """
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо {name}. Сообщение успешно отправлено")


class CategoryCreateView(CreateView):
    """Создание категории.

    Атрибуты:
        model: Модель категории.
        fields: Поля, доступные для ввода.
        template_name: Шаблон формы создания.
        success_url: URL редиректа после успешного создания.
    """

    model = Category
    form_class = CategoryForm
    template_name = 'catalog/category_form.html'
    success_url = reverse_lazy('catalog:categories_list')


class CategoryListView(ListView):
    """Список категорий.

    Атрибуты:
        model: Модель категории.
        template_name: Шаблон списка.
        context_object_name: Имя переменной контекста для списка категорий.
    """

    model = Category
    template_name = 'catalog/categories_list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    """Детальная страница категории.

    Атрибуты:
        model: Модель категории.
        template_name: Шаблон детальной страницы.
        context_object_name: Имя переменной контекста для категории.
    """

    model = Category
    template_name = 'catalog/category_detail.html'
    context_object_name = 'category'


class CategoryUpdateView(UpdateView):
    """Редактирование категории.

    Атрибуты:
        model: Модель категории.
        fields: Поля, доступные для редактирования.
        template_name: Шаблон формы редактирования.
        success_url: URL по умолчанию (может быть переопределён get_success_url()).
    """

    model = Category
    form_class = CategoryForm
    template_name = 'catalog/category_form.html'
    success_url = reverse_lazy('catalog:categories_list')

    def get_success_url(self):
        """URL для редиректа после успешного обновления.
        Ведёт на детальную страницу категории.
        """
        return reverse('catalog:category_detail', args={self.kwargs.get('pk')})


class CategoryDeleteView(DeleteView):
    """Удаление категории.

    Атрибуты:
        model: Модель категории.
        template_name: Шаблон подтверждения удаления.
        success_url: URL редиректа к списку категорий после удаления.
    """

    model = Category
    template_name = 'catalog/category_confirm_delete.html'
    success_url = reverse_lazy('catalog:categories_list')
