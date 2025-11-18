from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from account_app.models import Account

class RegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password',
    }))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password'
    }))

    class Meta():
        model = User
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = "Enter Email"
        self.fields['first_name'].widget.attrs['placeholder'] = "Enter FirstName"
        self.fields['last_name'].widget.attrs['placeholder'] = "Enter LastName"
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['repeat_password'].widget.attrs['class'] = 'form-control'
        for field in self.fields:
            if field not in ['password', 'repeat_password']:
                self.fields[field].widget.attrs['class'] = 'form-control'

class AccountsForm(ModelForm):
    phone_number = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter phone',
            'class': 'form-control',
        })
    )

    class Meta():
        model = Account
        fields = ('phone_number', 'pro_image')
        
    def __init__(self, *args, **kwargs):
        super(AccountsForm, self).__init__(*args, **kwargs)
        if 'pro_image' in self.fields:
            self.fields['pro_image'].widget.attrs['class'] = 'form-control'

