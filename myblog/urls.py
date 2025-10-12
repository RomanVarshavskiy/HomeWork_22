from django.urls import path

from myblog.apps import MyblogConfig
from myblog.views import (BlogPostCreateView, BlogPostDeleteView, BlogPostDetailView, BlogPostListView,
                          BlogPostUpdateView)

app_name = MyblogConfig.name

urlpatterns = [
    path("myblog/blogposts_list/", BlogPostListView.as_view(), name="blogposts_list"),
    path("myblog/blogpost_create/", BlogPostCreateView.as_view(), name="blogpost_create"),
    path("myblog/blogpost_detail/<int:pk>/", BlogPostDetailView.as_view(), name="blogpost_detail"),
    path("myblog/blogpost_update/<int:pk>/", BlogPostUpdateView.as_view(), name="blogpost_update"),
    path("myblog/blogpost_delete/<int:pk>/", BlogPostDeleteView.as_view(), name="blogpost_delete"),
]
