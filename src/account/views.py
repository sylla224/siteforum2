from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate, logout

# Create your views here.

User = get_user_model()


def creation_compte(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_created = User.objects.create_user(email=email, password=password)
        login(request, user_created)
        return redirect('forumapp:index')
    else:
        return render(request, template_name="account/signup.html")


def logout_user(request):
    logout(request)
    return redirect('forumapp:index')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('forumapp:index')
        else:
            return render(request, "account/login.html")

    else:
        return render(request, "account/login.html")
