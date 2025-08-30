from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Product


# Create your views here.
def home(request):
    # Берём последние 5 продуктов по полю created_at
    last_products = Product.objects.order_by("-created_at")[:5]

    # Выводим данные в консоль сервера (терминал, где запущен runserver)
    print("Последние 5 продуктов:")
    for p in last_products:
        print(f"- [{p.id}] {p.name} | создан: {p.created_at} | цена: {p.price}")

    return render(request, "home.html", {"last_products": last_products})


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо {name}. Сообщение успешно отправлено")
    return render(request, "contacts.html")
