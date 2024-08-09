from django import forms
from django.forms import BooleanField

from blog.models import Blog
from main.forms import StyleFormMixin


class BlogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ('owner','slug',)
