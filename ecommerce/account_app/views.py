from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegisterForm
from account_app.models import Account


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']

            if User.objects.filter(username=email).exists():
                messages.error(request, 'Энэ имэйл аль хэдийн бүртгэгдсэн байна.')
            else:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password
                )
                user.save()
                messages.success(request, 'Бүртгэл амжилттай! Одоо нэвтрэнэ үү.')
                return redirect('user_login')
        else:
            messages.error(request, 'Бүртгэлийн мэдээлэл буруу байна.')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})



# b. Нэвтрэх
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Та амжилттай нэвтэрлээ!')
            return redirect('home')  # Нүүр хуудас руу чиглүүлнэ
        else:
            messages.error(request, 'Имэйл эсвэл нууц үг буруу байна.')
            return redirect('user_login')
    return render(request, 'signin.html')


# c. Гарах
def user_logout(request):
    logout(request)
    messages.info(request, 'Та системээс гарлаа.')
    return redirect('user_login')
