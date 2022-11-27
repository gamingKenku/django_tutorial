from django import forms
from .models import BookStoreUser
from django.contrib.auth.forms import UserCreationForm, \
    AuthenticationForm, UsernameField


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Логин", max_length=50)
    first_name = forms.CharField(label="Имя пользователя", max_length=50)
    mail = forms.EmailField(label="Email", max_length=50)

    def save(self, commit=True):
        user = BookStoreUser.objects.create_user(
            self.cleaned_data.get("username"),
            self.cleaned_data.get("mail"),
            self.cleaned_data.get("first_name"),
            self.cleaned_data.get("password1")
        )

        if commit:
            user.save()
        return user

    class Meta:
        model = BookStoreUser
        fields = ['username', 'first_name', 'mail', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = UsernameField(
        label='Логин',
        widget=forms.TextInput(attrs={'autofocus': True}),
    )


class UserInfoChange(forms.ModelForm):
    username = forms.CharField(label="Логин", max_length=50, required=True)
    first_name = forms.CharField(label="Имя пользователя", max_length=50, required=True)
    mail = forms.EmailField(label="Email", max_length=50, required=True)

    class Meta:
        model = BookStoreUser
        fields = ['username', 'first_name', 'mail']
