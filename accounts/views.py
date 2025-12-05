from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from accounts.forms import RegisterForm
from accounts.models import Profile

from accounts.decorators import role_required
from events.models import Event
from groups.models import MinistryGroup
from attendance.models import AttendanceSheet, AttendanceRecord
from sermons.models import Sermon
from accounts.models import Profile


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


# list all users


def user_list(request):
    users = Profile.objects.all()
    return render(request, "accounts/user_list.html", {"users": users})


# Leader Dashbord


@role_required("leader")
def leader_dashboard(request):
    profile = request.user.profile
    group = profile.group  # leader's assigned group

    # safety :Leader must belong to a group
    if not group:
        return render(request, "accounts/no_group.html")

    # group members
    members = Profile.objects.filter(group=group)

    # group events
    group_events = Event.objects.filter(group=group).order_by("-date")[:5]

    # group sermons
    group_sermons = Sermon.objects.filter(group=group).order_by("-date")[:5]

    # group attendance Sheets
    sheets = AttendanceSheet.objects.filter(group=group).order_by("-date")[:10]

    context = {
        "group": group,
        "members": members,
        "group_events": group_events,
        "group_sermons": group_sermons,
        "sheets": sheets,
        "profile": profile,
    }
    return render(request, "accounts/leader_dashboard.html", context)
