import secrets
import string

from django import forms
from django.http import request
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail


from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm, UserPasswordRecoveryForm, UserUpdateForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    extra_context = {'title': 'Регистрация'}

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        code = secrets.token_hex(16)
        user.code = code
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{code}/'
        send_mail(subject='Подтверждение почты',
                  message=f'Пожалуйста подтверди корректность почтового адреаса {url}',
                  from_email=EMAIL_HOST_USER,
                  recipient_list=[user.email]
                  )

        return super().form_valid(form)


def email_verification(request, code):
    user = get_object_or_404(User, code=code)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))

class ResetPasswordView(TemplateView):
    model = User
    form_class = PasswordResetForm
    template_name = 'users/pass_reset.html'
    success_url = reverse_lazy('users:login')
    extra_context = {'title': 'Смена пароля'}

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_pass = User.objects.make_random_password(length=12)
            user.set_password(new_pass)
            user.save()
            send_mail(
                subject='Новый пароль',
                message=f'Ваш новый пароль: {new_pass}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email]
            )

            return redirect(reverse('users:login'))
        except User.DoesNotExist:
            return redirect(reverse('users:user_does_not_found'))



class UserDoesNotFound(TemplateView):
    model=User
    template_name = 'users/user_does_not_found.html'
    extra_context = {'title': 'Пользователь не найден'}


class ProfileView(LoginRequiredMixin, UpdateView):
    extra_context = {'title': 'Профиль'}
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')
    extra_context = {'title': 'Профиль'}

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "users/users_list.html"
    permission_required = 'users.view_user'
    extra_context = {'title': 'Пользователи'}

    def test_func(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return True
        return False

class UserUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = User
    template_name = "users/update_user.html"
    form_class = UserUpdateForm
    permission_required = ("users.can_deactivate_user",)
    success_url = reverse_lazy("users:users_list")
    extra_context = {'title': 'Изменение пользователя'}


# @login_required
# def block_user(request, pk):
#     """Блокировка пользователя менеджером"""
#     user = get_object_or_404(User, pk=pk)
#     if user.is_active:
#         user.is_active = False
#     else:
#         user.is_active = True
#     user.save()
#     return redirect(reverse('main:manager_view_user', kwargs={'pk': pk}))

#
