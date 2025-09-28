from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from catalog.models import Contact, Product, Category

from .forms import ProductForm, CategoryForm


def home(request):
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

def products_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/products_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product,id=product_id)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо {name}. Сообщение успешно отправлено")
    contacts = Contact.objects.all()  # получаем контакты из БД
    return render(request, "catalog/contacts.html", {"contacts": contacts})

def product_create(request):
    """
    Страница создания нового товара.
    Обрабатывает GET (показ формы) и POST (валидация и сохранение).
    """
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            # проставим даты, если они не заполнены
            today = timezone.now().date()
            if not product.created_at:
                product.created_at = today
            product.updated_at = today
            product.save()
            return redirect("catalog:product_detail", product_id=product.id)
    else:
        form = ProductForm()

    return render(request, "catalog/product_form.html", {"form": form})


def categories_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'catalog/categories_list.html', context)


def category_detail(request, category_id):
    category = get_object_or_404(Category,id=category_id)
    context = {'category': category}
    return render(request, 'catalog/category_detail.html', context)

def category_create(request, category=None):
    """
    Страница создания новой категории товара.
    Обрабатывает GET (показ формы) и POST (валидация и сохранение).
    """
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            return redirect("catalog:category_detail", category_id=category.id)
    else:
        form = CategoryForm()

    return render(request, "catalog/category_form.html", {"form": form})
