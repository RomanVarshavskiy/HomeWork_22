from django.urls import path

from myblog.views import BlogPostCreateView, BlogPostListView, BlogPostDetailView, BlogPostUpdateView, \
    BlogPostDeleteView
from myblog.apps import MyblogConfig

app_name = MyblogConfig.name

urlpatterns = [
    # path("myblog/", home, name="home"),
    path("myblog/blogposts_list/", BlogPostListView.as_view(), name="blogposts_list"),
    path("myblog/blogpost_create/", BlogPostCreateView.as_view(), name="blogpost_create"),
    path("myblog/blogpost_detail/<int:pk>/", BlogPostDetailView.as_view(), name="blogpost_detail"),
    path("myblog/blogpost_update/<int:pk>/", BlogPostUpdateView.as_view(), name="blogpost_update"),
    path("myblog/blogpost_delete/<int:pk>/", BlogPostDeleteView.as_view(), name="blogpost_delete"),

]
