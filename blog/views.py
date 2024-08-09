from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from pytils.translit import slugify
from blog.models import Blog
from blog.forms import BlogForm

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    extra_context = {'title': 'Публикации'}

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(published=True)

        return queryset


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:blogs')
    extra_context = {'title': 'Новая публикация'}

    def form_valid(self, form):
        blog = form.save()
        blog.owner = self.request.user
        blog.slug = slugify(blog.header)
        blog.save()

        return super().form_valid(form)

class BlogDetailView(DetailView):
    model = Blog
    extra_context = {'title': 'Публикация'}

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count += 1
        self.object.save()

        return self.object


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:blogs')
    extra_context = {'title': 'Изменение публикации'}

    def form_valid(self, form):
        blog = form.save()
        blog.slug = slugify(blog.header)
        blog.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blogs')
    extra_context = {'title': 'Удаление публикации'}