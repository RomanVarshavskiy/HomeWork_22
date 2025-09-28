from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, home, product_create, product_detail, products_list, categories_list, \
    category_detail, category_create

app_name = CatalogConfig.name

urlpatterns = [
    path("catalog/", home, name="home"),
    path("catalog/contacts/", contacts, name="contacts"),
    path("catalog/products_list/", products_list, name="products_list"),
    path("catalog/product_create/", product_create, name="product_create"),
    path("catalog/product_detail/<int:product_id>", product_detail, name="product_detail"),
    path("catalog/category_create/", category_create, name="category_create"),
    path("catalog/categories_list/", categories_list, name="categories_list"),
    path("catalog/category_detail/<int:category_id>", category_detail, name="category_detail"),
]
