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

from django.db.models import Q
from django.contrib.auth.decorators import login_required
from sermons.views import pastor_required
from django.utils import timezone


# views / routes


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            role = user.profile.role

            redirect_map = {
                "admin": "dashboard:index",
                "pastor": "accounts:pastor_dashboard",
                "leader": "accounts:leader_dashboard",
                "member": "accounts:member_dashboard",
            }

            return redirect(redirect_map.get(role, "dashboard:index"))

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


@login_required
@pastor_required
def pastor_dashboard(request):
    profile = request.user.profile

    if profile.role != "pastor":
        return redirect("dashboard:index")

    # Pastors own sermons

    sermons = Sermon.objects.filter(Q(preacher=request.user) | Q(group=None)).order_by(
        "-date"
    )
    my_group = profile.group
    global_events = Event.objects.filter(event_type="global").order_by("-date")
    group_events = Event.objects.filter(group=profile.group).order_by("-date")
    events = Event.objects.filter(
        Q(group=profile.group) | Q(event_type="global")
    ).order_by("-date")
    # approvals = EventRequest.objects.filter(status="pending") # TODO add event request app

    return render(
        request,
        "accounts/pastor_dashboard.html",
        {
            "sermons": sermons,
            "events": events,
            "global_events": global_events,
            "group_events": group_events,
            "my_group": my_group,
            #  "approvals": approvals,
        },
    )


# member dashboard
@login_required
def member_dashboard(request):
    profile = request.user.profile
    group = profile.group

    # safety :Leader must belong to a group
    if not group:
        return render(request, "accounts/no_group.html")

    # 1. Sermons : global + group specific
    sermons = Sermon.objects.filter(Q(group=group) | Q(group=None)).order_by("-date")

    # 2. Events : global + group specific
    today = timezone.now().date()
    events = Event.objects.filter(
        Q(group=group) | Q(event_type="global"), date__gte=today
    ).order_by("date")

    # 3. Attendance Summary (last 5)
    records = (
        AttendanceRecord.objects.filter(user=request.user)
        .select_related("attendance")
        .order_by("-attendance__date")[:5]
    )

    # 4. group Information in the profile.group

    context = {
        "profile": profile,
        "sermons": sermons,
        "events": events,
        "records": records,
        "attendance_records": records,
    }
    return render(request, "accounts/member_dashboard.html", context)
