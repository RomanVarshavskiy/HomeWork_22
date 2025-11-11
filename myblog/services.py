from django.core.cache import cache

from myblog.models import BlogPost
from config.settings import CACHE_ENABLED

def get_blogpost_from_cache():
    """Получает данные по статьям из кэша, если кэш пустой, получает данные из БД"""
    if not CACHE_ENABLED:
        return BlogPost.objects.filter(is_published=True)
    key = "blogposts_list_published"
    blogposts = cache.get(key)
    if blogposts is not None:
        return blogposts
    blogposts = BlogPost.objects.filter(is_published=True)
    cache.set(key, blogposts)
    return blogposts
