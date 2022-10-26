from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms
class LoginForm(AuthenticationForm):
    class Meta(object):
        model = User
        fields = ('username', 'password')
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Логин"
        self.fields['password'].label = "Пароль"