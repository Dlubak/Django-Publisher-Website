from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.shortcuts import redirect, render
from django.conf import settings

# Create your views here.
from .forms import CreateUserForm
from blog.models import Article


def registerPage(request):
    if request.method != "POST":
        form = CreateUserForm()
    else:
        form = CreateUserForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect('authenticate:login')
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
                print(settings.LOGIN_REDIRECT_URL)
                print(request.POST.get('next'))
                return redirect(request.POST.get('next'))
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


@login_required(login_url='/login')
def profilePage(request):
    """
    Display a user's profile
    """
    print(request)
    context = {
        'profile': request.user,
        'articles': Article.objects.all()  # (author=request.user).order_by('pub_date')
    }
    return render(request, 'authentication/profile.html', context)
