from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False,
                                   help_text='Необязательное поле.',
                                   widget=forms.TextInput(attrs={
                                       "class": "form-control",
                                       "placeholder": "Введите ваш номер телефона"
                                   }))
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Имя пользователя"}))
    usable_password = None

    class Meta:
        model = CustomUser
        fields = ("email", "username", "phone_number", "password1", "password2")
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Электронная почта"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.label = ""  # скрыть label
        self.fields["password1"].help_text = ""
        self.fields["password1"].widget = forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Пароль"
        })

        self.fields["password2"].help_text = ""
        self.fields["password2"].widget = forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Подтвердите пароль"
        })

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Номер телефона должен содержать только цифры.')
        return phone_number


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Электронная почта"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Пароль"})
    )

    class Meta:
        model = CustomUser
        fields = ("username", "password1")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.label = ""  # скрыть label
        self.fields["username"].help_text = ""
        self.fields["password"].help_text = ""

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email", "username", "phone_number", "avatar", "country")
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Электронная почта"}),
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя пользователя"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Телефон"}),
            "country": forms.TextInput(attrs={"class": "form-control", "placeholder": "Страна"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.label = ""