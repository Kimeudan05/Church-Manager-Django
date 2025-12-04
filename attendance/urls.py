from django.urls import path
from . import views


app_name = "attendance"
urlpatterns = [
    path("", views.attendance_list, name="attendance_list"),
    path("create/", views.attendance_create, name="attendance_create"),
    path("<int:sheet_id>/mark/", views.attendance_mark, name="attendance_mark"),
    path("<int:id>/edit/", views.attendance_edit, name="attendance_edit"),
    path("<int:id>/delete/", views.attendance_delete, name="attendance_delete"),
    # Export attendance
    path(
        "export/excel/", views.export_attendance_excel, name="attendance_export_excel"
    ),
    path("export/pdf/", views.create_attendance_pdf, name="attendance_export_pdf"),
]
