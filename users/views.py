import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import CustomUser


class RegisterView(CreateView):

    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message = f"Для завершения регистрации, перейдите по ссылке {url}",
            from_email = EMAIL_HOST_USER,
            recipient_list = [user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = "users/profile_edit.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("users:profile_edit")


# class RegisterView(CreateView):
#     template_name = 'users/register.html'
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('library:books_list')

    # def form_valid(self, form):
    #     user = form.save()
    #     self.send_welcome_email(user.email)
    #
    #     return super().form_valid(form)

    #
    # def send_welcome_email(self, user_email):
    #     subject = 'Добро пожаловать в наш магазин!'
    #     message = 'Спасибо, что зарегистрировались в нашем магазине!'
    #     from_email = 'raman.varshavskiy2@gmail.com'
    #     recipient_list = [user_email,]
    #     send_mail(subject, message, from_email, recipient_list)