
from django.conf import settings
from django.core.cache import cache
from blog.models import Blog



def get_blog_list():
    """ Берем из кэша список публикаций, если кэш пуст, то записываем список публикаций в БД"""

    if settings.CACHE_ENABLED:
        key = 'blog_list'
        blog = cache.get(key)
        if blog is None:
            blogs = Blog.objects.all()
            cache.set(key, blogs)
    else:
        blogs = Blog.objects.all()
    return blogs


