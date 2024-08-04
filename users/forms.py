from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from users.models import User
from main.forms import StyleFormMixin, StyleMixin

class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

class UserProfileForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model =User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'is_active',)


class UserPasswordRecoveryForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

class UserUpdateForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = User
        fields = ("is_active",)


# class UserRegisterForm(StyleFormMixin, UserCreationForm):
#
#     class Meta:
#         model = User
#         fields = ('email', 'password1', 'password2')
# class UserProfileForm(StyleFormMixin, UserChangeForm):
#
#     class Meta:
#         model =User
#         fields = ('email', 'first_name', 'last_name', 'avatar')
#
# class UserPasswordRecoveryForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('email',)
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs["class"] = "form-control"
#
# class LoginCustomForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs["class"] = "form-control"
# class UserUpdateForm():
#     class Meta:
#         model = User
#         fields = ("is_active",)
#
#
