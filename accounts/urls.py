from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("user-list/", views.user_list, name="user_list"),
    path("leader/", views.leader_dashboard, name="leader_dashboard"),
    path("pastor-dashboard/", views.pastor_dashboard, name="pastor_dashboard"),
    path("member-dashboard/", views.member_dashboard, name="member_dashboard"),
]
