import random
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from config.settings import EMAIL_HOST_USER
from users.forms import UserAuthenticationForm, UserProfileForm, UserRegisterForm
from users.models import User
from django.contrib.auth import login
from users.service import send_email_for_verify
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin



User = get_user_model()

class LoginView(BaseLoginView):
    form_class = UserAuthenticationForm


class LogoutView(BaseLogoutView):
    template_name = 'users/logout.html'


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('mailing:mailing_list')
        return redirect('users:invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user


class RegistrView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user=form.save()
            user.is_active = False
            user.save()
            send_email_for_verify(request, user)
            return redirect('users:confirm_email')
        return redirect(reverse('users:login'))


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('user_email')
        try:
            user = User.objects.get(email=email)
            random_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
            send_mail(subject='new_password', message=f'{random_password}', from_email=EMAIL_HOST_USER, recipient_list=[user.email])
            user.set_password(random_password)
            user.save()
            return redirect(reverse('users:login'))
        except Exception:
            message = 'Мы не нашли такого пользователя'
            context = {
                'message': message,
            }
            return render(request, 'users/forgot_password.html', context)
    else:
        return render(request, 'users/forgot_password.html')
