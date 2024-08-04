from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from users.views import RegisterView, ProfileView, email_verification, ResetPasswordView, UserDoesNotFound, UserListView, UserUpdateView
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('email-confirm/<str:code>/', email_verification, name='email-confirm'),
    path('pass_reset/', ResetPasswordView.as_view(), name='pass_reset'),
    path('user_does_not_found/', UserDoesNotFound.as_view(), name='user_does_not_found'),
    path("users_list/", UserListView.as_view(), name="users_list"),
    path("update_user/<int:pk>/", UserUpdateView.as_view(), name="update_user"),

]

# from django.urls import path, include
#
# from django.contrib.auth.views import LoginView, LogoutView
# from users.views import UserCreateView, UserListView, UserUpdateView, UpdateView, UserRegisterForm, UserUpdateForm, email_verification, RegisterMessageView
# from users.apps import UsersConfig
# from users.forms import LoginCustomForm
#
# app_name = UsersConfig.name
#
# urlpatterns = [
#     path('', LoginView.as_view(template_name="users/login.html", form_class=LoginCustomForm), name='login'),
#     path("register/", UserCreateView.as_view(), name="register"),
#     path("email_confirm/<str:code>/", email_verification, name="email_confirm"),
#     path("register/message/", RegisterMessageView.as_view(), name="register_message"),
#     path("users_list/", UserListView.as_view(), name="users_list"),
#     path("update_user/<int:pk>/", UserUpdateView.as_view(), name="update_user"),
#     path('logout/', LogoutView.as_view(), name='logout'),
#
# ]
