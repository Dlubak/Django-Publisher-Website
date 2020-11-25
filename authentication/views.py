from blog.models import Article
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, UserCreationForm)
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from .decorators import unauthenticated_user, check_owner_or_admin
from .forms import CreateUserForm, UpdateProfileForm, UpdateUserForm


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


def profilePage(request, username):
    """
    Display a user's profile
    """
    user = get_object_or_404(User, username=username)
    context = {
        'profilePage': user
    }
    if request.user == user or request.user.is_superuser:
        articles = Article.objects.filter(
            author=user).order_by('pub_date')
        context['articles'] = articles
    return render(request, 'authentication/profile.html', context)


@login_required(login_url='/login')
def updateProfile(request, username):
    template_name = "authentication/update_profile.html"
    user = get_object_or_404(User, username=username)
    if request.method != 'POST':
        u_form = UpdateUserForm(instance=user)
        p_form = UpdateProfileForm(instance=user.profile)
    else:
        u_form = UpdateUserForm(instance=user, data=request.POST)
        p_form = UpdateProfileForm(
            instance=user.profile,
            data=request.POST,
            files=request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('authentication:profile', username=username)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, template_name, context)
