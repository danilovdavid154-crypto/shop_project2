from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import EmailUpdateForm, RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:product_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно. Вы вошли в аккаунт.')
            return redirect('catalog:product_list')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = EmailUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен.')
            return redirect('accounts:profile')
    else:
        form = EmailUpdateForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})
