from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import EmailVerify, RegistrView, ProfileView, forgot_password
from django.views.decorators.cache import cache_page



app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('invalid_verify/', TemplateView.as_view(template_name='users/invalid_verify.html'), name='invalid_verify'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),
    path('confirm_email/', TemplateView.as_view(template_name='users/confirm_email.html'), name='confirm_email'),
    path('register/', RegistrView.as_view(), name='register'),
    path('forgot/', forgot_password, name='forgot'),
    path('profile/', cache_page(60)(ProfileView.as_view()), name='profile'),
]
