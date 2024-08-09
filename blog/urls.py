from django.urls import path, include
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogUpdateView, BlogDetailView, BlogCreateView, BlogDeleteView


app_name = BlogConfig.name

urlpatterns = [
    path('blogs/', BlogListView.as_view(), name='blogs'),
    path('blog_create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog_update/<int:pk>', BlogUpdateView.as_view(), name='blog_update'),
    path('blog_detail/<int:pk>', cache_page(60)(BlogDetailView.as_view()), name='blog_detail'),
    path('blog/delete/<int:pk>', BlogDeleteView.as_view(), name='confirm_delete'),

]
