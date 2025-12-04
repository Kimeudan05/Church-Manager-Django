from django.urls import path
from . import views

app_name = "sermons"

urlpatterns = [
    path("", views.sermons_list, name="list"),
    path("create/", views.sermon_create, name="create"),
    path("<int:pk>/update/", views.sermon_update, name="update"),
    path("<int:pk>/delete/", views.sermon_delete, name="delete"),
    path("<int:pk>/detail/", views.sermon_detail, name="detail"),
]
