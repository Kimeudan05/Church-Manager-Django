from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
from .models import Attendance, AttendanceRecord
from groups.models import MinistryGroup
from .forms import AttendanceForm, MarkAttendanceForm


@login_required
def attendance_list(request):
    records = Attendance.objects.all().order_by("-date")
    return render(request, "attendance/list.html", {"records": records})


@login_required
def attendance_create(request):
    form = AttendanceForm(request.POST)
    if form.is_valid():
        attendance = form.save(commit=False)
        attendance.recorded_by = request.user
        attendance.save()
        return redirect("attendance:mark", attendance.id)

    else:
        form = AttendanceForm()

    return render(request, "attendance/create.html", {"form": form})


@login_required
def attendance_mark(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)

    # choose users based on group
    if attendance.group:
        users = User.objects.filter(profile__role="member")
    else:
        users = User.objects.all()

    # get initial values
    present_initial = AttendanceRecord.objects.filter(
        attendance=attendance, present=True
    ).values_list("user_id", flat=True)

    if request.method == "POST":
        form = MarkAttendanceForm(
            users=users, initial_present=present_initial, data=request.POST
        )

        if form.is_valid():
            total = 0
            for user in users:
                is_present = form.cleaned_data.get(f"user_{user.id}", False)

                AttendanceRecord.objects.update_or_create(
                    attendance=attendance,
                    user=user,
                    defaults={"present": is_present},
                )

                if is_present:
                    total += 1

            attendance.total_present = total
            attendance.save()

            messages.success(request, "Attendance updated!")
            return redirect("attendance:list")

    else:
        form = MarkAttendanceForm(users=users, initial_present=present_initial)

    return render(
        request,
        "attendance/mark.html",
        {"form": form, "attendance": attendance},
    )
