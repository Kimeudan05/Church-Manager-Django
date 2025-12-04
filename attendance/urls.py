from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [
    path("", views.attendance_list, name="list"),
    path("create/", views.attendance_create, name="create"),
    path("<int:attendance_id>/mark/", views.attendance_mark, name="mark"),
]
