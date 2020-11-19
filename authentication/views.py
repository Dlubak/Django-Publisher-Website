from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Create your views here.
from .forms import CreateUserForm


def registerPage(request):
    if request.method != "POST":
        form = CreateUserForm()
    else:
        form = CreateUserForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('blog:index')
    context = {"form": form}
    return render(request, 'authentication/register.html', context)


def loginPage(request):
    if request.method != "POST":
        form = AuthenticationForm()
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog:index')
    context = {'form': form}
    return render(request, 'authentication/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('blog:index')
