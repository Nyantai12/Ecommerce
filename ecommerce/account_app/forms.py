# forms.py
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from account_app.models import Account

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

class RegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Нууц үг оруулна уу',
        'class': 'form-control'
    }))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Нууц үгээ давтан оруулна уу',
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')
        if password and repeat_password and password != repeat_password:
            self.add_error('repeat_password', 'Нууц үг таарахгүй байна.')



class AccountsForm(ModelForm):
    phone_number = forms.CharField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Утасны дугаар оруулна уу',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Account
        fields = ('phone_number', 'pro_image')
