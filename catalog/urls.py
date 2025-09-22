from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, home, product_detail, products_list, product_create


app_name = CatalogConfig.name

urlpatterns = [
    path("catalog/", home, name="home"),
    path("catalog/contacts/", contacts, name="contacts"),
    path("catalog/products_list/", products_list, name="products_list"),
    path("catalog/product_detail/<int:product_id>", product_detail, name="product_detail"),
    path("catalog/product_create/", product_create, name="product_create"),
]
