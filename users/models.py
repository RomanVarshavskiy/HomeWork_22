from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    userName = None
    email = models.EmailField(unique=True, verbose_name="Email")

    phone_number = PhoneNumberField(verbose_name="Телефон", blank=True, null=True, help_text="Введите номер телефона")
    avatar = models.ImageField(upload_to="users/avatars", verbose_name="Аватар", blank=True, null=True, help_text="Загрузите свой аватар")
    country = models.CharField(verbose_name="Страна", blank=True, null=True, help_text="Укажите свою страну")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
