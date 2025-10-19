from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.mail import send_mail
from .forms import CustomUserCreationForm
from .models import CustomUser


class RegisterView(CreateView):

    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        self.send_welcome_email(user.email)

        return super().form_valid(form)


# class RegisterView(CreateView):
#     template_name = 'users/register.html'
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('library:books_list')

    # def form_valid(self, form):
    #     user = form.save()
    #     self.send_welcome_email(user.email)
    #
    #     return super().form_valid(form)


    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш магазин!'
        message = 'Спасибо, что зарегистрировались в нашем магазине!'
        from_email = 'raman.varshavskiy2@gmail.com'
        recipient_list = [user_email,]
        send_mail(subject, message, from_email, recipient_list)