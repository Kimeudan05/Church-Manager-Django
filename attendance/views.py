from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
from .models import AttendanceSheet, AttendanceRecord
from groups.models import MinistryGroup
from .forms import AttendanceSheetForm, MarkAttendanceForm, AttendanceFilterForm
from events.models import Event
from sermons.models import Sermon

### Create the attendance sheet ###


@login_required
def attendance_create(request):
    profile = request.user.profile
    if profile.role == "member":
        return redirect("dashboard:index")  # or 403

    if request.method == "POST":
        form = AttendanceSheetForm(request.POST)
        if form.is_valid():
            sheet = form.save(commit=False)
            sheet.recorded_by = request.user

            # force group leader to their group
            if profile.role == "leader":
                sheet.group = profile.group

            sheet.save()
            return redirect("attendance:attendance_mark", sheet_id=sheet.id)

    else:
        form = AttendanceSheetForm()

        # Limit list for leaders
        if profile.role == "leader":
            form.fields["group"].queryset = MinistryGroup.objects.filter(
                id=profile.group.id
            )
            form.fields["event"].queryset = Event.objects.filter(group=profile.group)
            form.fields["sermon"].queryset = Sermon.objects.filter(group=profile.group)

    return render(request, "attendance/create.html", {"form": form})


### List All sheets with filters,


@login_required
def attendance_list(request):
    profile = request.user.profile
    if profile.is_admin_or_pastor():
        sheets = AttendanceSheet.objects.all()
    else:
        sheets = AttendanceSheet.objects.filter(group=profile.group)

    sheets = sheets.order_by("-date")

    # filtering but limit options for leaders

    form = AttendanceFilterForm(request.GET or None)

    if profile.role == "leader":
        form.fields["group"].queryset = MinistryGroup.objects.filter(
            id=profile.group.id
        )
        form.fields["event"].queryset = Event.objects.filter(group=profile.group)
        form.fields["sermon"].queryset = Sermon.objects.filter(group=profile.group)

    if form.is_valid():
        if form.cleaned_data["date_from"]:
            sheets = sheets.filter(date__gte=form.cleaned_data["date_from"])

        if form.cleaned_data["date_to"]:
            sheets = sheets.filter(date__lte=form.cleaned_data["date_to"])

        if form.cleaned_data["type"]:
            sheets = sheets.filter(type=form.cleaned_data["type"])

        # (leader filter restricted above)
        if form.cleaned_data["group"]:
            sheets = sheets.filter(group=form.cleaned_data["group"])

        if form.cleaned_data["sermon"]:
            sheets = sheets.filter(sermon=form.cleaned_data["sermon"])

        if form.cleaned_data["event"]:
            sheets = sheets.filter(event=form.cleaned_data["event"])

    return render(
        request, "attendance/attendance_list.html", {"sheets": sheets, "form": form}
    )


##### Mark Attendance ####


@login_required
def attendance_mark(request, sheet_id):
    sheet = get_object_or_404(AttendanceSheet, id=sheet_id)

    profile = request.user.profile

    # Leader only mark attendance for their group
    if profile.role == "leader" and sheet.group != profile.group:
        messages.error(request, "Unauthorized access to this attendance sheet.")
        return redirect("attendance:attendance_list")

    # Limit sers to group members for leader
    if profile.is_admin_or_pastor():
        users = User.objects.all().order_by("username")
    else:
        users = User.objects.filter(profile__group=profile.group).order_by("username")

    # get already marked attendance
    initial_present_ids = AttendanceRecord.objects.filter(
        attendance=sheet, present=True
    ).values_list("user_id", flat=True)

    if request.method == "POST":
        form = MarkAttendanceForm(users, initial_present_ids, request.POST)

        if form.is_valid():
            # save records
            total = 0
            AttendanceRecord.objects.filter(attendance=sheet).delete()

            for user in users:
                is_present = form.cleaned_data.get(f"user_{user.id}", False)

                AttendanceRecord.objects.create(
                    attendance=sheet, user=user, present=is_present
                )

                if is_present:
                    total += 1

            sheet.total_present = total
            sheet.save()
            return redirect("attendance:attendance_list")

    else:
        form = MarkAttendanceForm(users, initial_present_ids)

    return render(
        request, "attendance/mark_attendace.html", {"form": form, "sheet": sheet}
    )


# editing and delete attendance sheet
@login_required
def attendance_edit(request, id):
    sheet = get_object_or_404(AttendanceSheet, id=id)
    profile = request.user.profile

    if profile.role == "leader" and sheet.group != profile.group:
        messages.error(request, "Unauthorized access to this attendance sheet.")
        return redirect("attendance:attendance_list")

    form = AttendanceSheetForm(request.POST or None, instance=sheet)

    if form.is_valid():
        form.save()
        messages.success(request, "Attendance Sheet Updated")
        return redirect("attendance:attendance_list")

    return render(request, "attendance/edit.html", {"form": form, "sheet": sheet})


# Delete The Sheet
@login_required
def attendance_delete(request, id):
    sheet = get_object_or_404(AttendanceSheet, id=id)

    if request.method == "POST":
        sheet.delete()
        messages.success(request, "Attendance Sheet deleted!")
        return redirect("attendance:attendance_list")

    return render(request, "attendance/delete_confirm.html", {"sheet": sheet})


### Exporting Pdf And excel
import openpyxl
from django.http import HttpResponse


@login_required
def export_attendance_excel(request):
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Attendance"

    sheet.append(["Date", "Type", "Group", "Sermon", "Event", "Total Attendance"])

    for att in AttendanceSheet.objects.all():
        sheet.append(
            [
                att.date,
                att.get_type_display(),
                att.group.name if att.group else "",
                att.sermon.title if att.sermon else "",
                att.event.title if att.event else "",
                att.total_present,
            ]
        )
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officdocument.spreadsheetml.sheet"
        )
    response["Content-Disposition"] = "attachment; filename = attendance.xlsx"
    wb.save(response)
    return response


# pdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


@login_required
def create_attendance_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=attendance.pdf"

    p = canvas.Canvas(response, pagesize=A4)
    y = 800

    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, 820, "Attendance Report")

    p.setFont("Helvetica", 10)

    for att in AttendanceSheet.objects.all():
        line = f"{att.date} | {att.get_type_display()} | {att.total_present}"
        p.drawString(50, y, line)
        y -= 20

        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 10)
            y = 800

    p.save()
    return response
