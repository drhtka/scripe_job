# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout, get_user_model
from accounts.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm
from django.contrib import messages
# Create your views here.
User = get_user_model()

def login_view(request):
    # в эту функцию  валидные данные провереные в форме
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data # получаем вадидные данные
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)# атентифицируем пользователя
        # print('user')
        # print(user)
        login(request, user)
        request.session['my_list'] = email
        # print('em')
        # print(request.session['my_list'])

        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})# если форма не заполнена

def logout_view(request):
    # выход
    logout(request)
    return redirect('home')

def register_view(request):
    # регистрация
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])# password тот текст который ввел пользователь в полле пароля
        new_user.save()
        messages.success(request, 'Пользователь добавлен в систему.')
        return render(request, 'accounts/register_done.html',
                      {'new_user': new_user})# созданный юзер
    return render(request, 'accounts/register.html', {'form': form})# возвращаем на форму


def update_view(request):
    if request.user.is_authenticated:
        user = request.user# проверяем зарегестрировался ли пользователь
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)# получив данные из формы, изменить значение в этом юзере
            if form.is_valid():# если форма валидна
                data = form.cleaned_data
                user.city = data['city']# берем данные из data
                user.language = data['language']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'Данные сохраненны.')
                return redirect('accounts:update')
        form = UserUpdateForm(# нполняем форму начальными значениями котры есть у юзера
            initial={'city': user.city, 'language': user.language,
                     'send_email': user.send_email})
        return render(request, 'accounts/update.html',
                      {'form': form})
    else:
        return redirect('accounts:login')# если нет перенаправить на страницу входа

def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)# получем юзера который зарегистрировался и удаляем по pk
            qs.delete()
            messages.error(request, 'Пользователь удален :(')
    return redirect('home')