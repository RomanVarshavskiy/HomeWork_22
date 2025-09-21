from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Product, Contact


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
    product = Product.objects.get(id=product_id)
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

