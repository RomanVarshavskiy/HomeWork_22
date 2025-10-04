from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ContactsView, home, ProductCreateView, ProductListView, ProductDetailView, ProductUpdateView, \
    ProductDeleteView, CategoryCreateView, CategoryListView, CategoryDetailView, CategoryUpdateView, CategoryDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path("catalog/", home, name="home"),
    path("catalog/products_list/", ProductListView.as_view(), name="products_list"),
    path("catalog/product_create/", ProductCreateView.as_view(), name="product_create"),
    path("catalog/product_detail/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("catalog/product_update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"),
    path("catalog/product_delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"),
    path("catalog/category_create/", CategoryCreateView.as_view(), name="category_create"),
    path("catalog/categories_list/", CategoryListView.as_view(), name="categories_list"),
    path("catalog/category_detail/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path("catalog/category_update/<int:pk>/", CategoryUpdateView.as_view(), name="category_update"),
    path("catalog/category_delete/<int:pk>/", CategoryDeleteView.as_view(), name="category_delete"),
    path("catalog/contacts/", ContactsView.as_view(), name="contacts"),
]
