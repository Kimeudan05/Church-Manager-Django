from django.urls import reverse


def role_context(request):
    dashboard_map = {
        "admin": "dashboard:index",
        "pastor": "accounts:pastor_dashboard",
        "leader": "accounts:leader_dashboard",
        "member": "accounts:member_dashboard",
    }
    if request.user.is_authenticated:
        try:
            role = request.user.profile.role
            dashboard_url = reverse(dashboard_map.get(role, "dashboard:index"))

            profile = request.user.profile
            return {
                "role": role,
                "user_profile": profile,
                "user_group": profile.group,
                "dashboard_url": dashboard_url,
            }

        except:
            return {
                "role": None,
                "user_profile": None,
                "user_group": None,
                "dashboard_url": None,
            }
    return {
        "role": None,
        "user_profile": None,
        "user_group": None,
        "dashboard_url": reverse("dashboard:index"),
    }
