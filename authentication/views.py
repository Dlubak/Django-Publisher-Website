from blog.models import Article
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, UserCreationForm)
from django.shortcuts import redirect, render

from .decorators import unauthenticated_user
from .forms import CreateUserForm


# Create your views here.
def registerPage(request):
    if request.method != "POST":
        form = CreateUserForm()
    else:
        form = CreateUserForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect('authentication:login')
    context = {"form": form}
    return render(request, 'authentication/register.html', context)


@unauthenticated_user
def loginPage(request):
    nextPage = request.POST.get('next')
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
                if nextPage:
                    return redirect(nextPage)
                return redirect('blog:index')
    context = {'form': form}
    return render(request, 'authentication/login.html', context)
 

@login_required(login_url="/login")
def logoutPage(request):
    logout(request)
    return redirect('blog:index')

# TODO:
# @login_required
# def changePassword(request):
#     return render(request, 'authentication/change_password_form.html', {})


def profilePage(request):
    """
    Display a user's profile
    """
    print(request)
    context = {
        'profile': request.user,
        'articles': Article.objects.filter(author=request.user).order_by('pub_date')
    }
    return render(request, 'authentication/profile.html', context)
