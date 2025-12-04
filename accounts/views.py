from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from accounts.forms import RegisterForm


# views / routes


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard:index")
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("accounts:login")


# def register_view(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Account created successfully.")
#             return redirect("accounts:login")

#         username = request.POST.get("username")
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists")
#             return redirect("accounts:register")

#         user = User.objects.create_user(
#             username=username, email=email, password=password
#         )

#         # Assign default role
#         member_group = Group.objects.get(name="Member")
#         user.groups.add(member_group)

#         messages.success(request, "Account created! Please log in.")
#         return redirect("accounts:login")

#     return render(request, "accounts/register.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Assign default role
            member_group, created = Group.objects.get_or_create(name="Member")
            user.groups.add(member_group)

            messages.success(request, "Account created successfully.")
            return redirect("accounts:login")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})
