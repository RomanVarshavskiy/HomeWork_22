from django.contrib import admin

from myblog.models import BlogPost  # название модели


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "content",
        "preview_image",
        "created_at",
        "updated_at",
        "is_published",
    )
    list_filter = (
        "title",
        "created_at",
        "is_published",
    )
    search_fields = (
        "title",
    )
