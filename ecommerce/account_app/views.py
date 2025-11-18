from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ValidationError

from account_app.models import Account
from .forms import RegisterForm, AccountsForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
# Create your views here.
def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        account_form = AccountsForm(request.POST, request.FILES)
        
        if form.is_valid() and account_form.is_valid():
            # Check if passwords match
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            
            if password != repeat_password:
                messages.error(request, 'Passwords do not match!')
                return render(request, 'register.html', {'form': form, 'account_form': account_form})
            
            # Validate password strength
            try:
                validate_password(password)
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
                return render(request, 'register.html', {'form': form, 'account_form': account_form})
            
            # Check if user with this email already exists
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.error(request, 'An account with this email already exists!')
                return render(request, 'register.html', {'form': form, 'account_form': account_form})
            
            # Check if username already exists
            if User.objects.filter(username=form.cleaned_data['email']).exists():
                messages.error(request, 'An account with this email already exists!')
                return render(request, 'register.html', {'form': form, 'account_form': account_form})
            
           
           
            phone_number = account_form.cleaned_data.get('phone_number')
            if Account.objects.filter(phone_number=phone_number).exists():
                messages.error(request, 'This phone number is already registered!')
                return render(request, 'register.html', {'form': form, 'account_form': account_form})
            
            try:
                # Create user
                user = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    password=password
                )
                
                # Create account
                account = account_form.save(commit=False)
                account.user = user
                account.save()
                
                messages.success(request, 'Registration successful! Please login.')
                return redirect('signin')
            except Exception as e:
                messages.error(request, f'An error occurred during registration: {str(e)}')
                return render(request, 'register.html', {'form': form, 'account_form': account_form})
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
        account_form = AccountsForm()
    
    return render(request, 'register.html', {'form': form, 'account_form': account_form})


def user_login(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')  # email эсвэл phone number
        password = request.POST.get('password')

        if identifier and password:
            user = None
            # 1. Identifier нь email байх эсэхийг шалгах
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                # 2. Identifier нь утасны дугаар байх эсэхийг шалгах
                try:
                    account = Account.objects.get(phone_number=identifier)
                    user = account.user
                except Account.DoesNotExist:
                    user = None

            if user:
                # password шалгах
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('index')
                else:
                    messages.error(request, 'Invalid password!')
            else:
                messages.error(request, 'User not found!')
        else:
            messages.error(request, 'Please fill in all fields!')

    return render(request, 'signin.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('signin')
