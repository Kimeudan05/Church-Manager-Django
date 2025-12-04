from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
from accounts.models import Profile
from groups.models import MinistryGroup
from events.models import Event
from sermons.models import Sermon


@login_required
def dashboard_view(request):
    user = request.user
    role = getattr(user.profile, "role", "member")  # default to member
    group = getattr(user.profile, "group", "")
    context = {
        "role": role,
        "group": group,
    }
    # Admin sees all
    if role == "admin":
        context.update(
            {
                "total_users": Profile.objects.count(),
                "total_groups": MinistryGroup.objects.count(),
                "total_events": Event.objects.count(),
                "total_sermons": Sermon.objects.count(),
                "upcoming_events": Event.objects.order_by("date")[:5],
                "latest_sermons": Sermon.objects.order_by("-date")[:5],
            }
        )

    # Pastor sees sermons they preached + all global events
    elif role == "pastor":
        context.update(
            {
                "my_sermons": Sermon.objects.filter(preacher=user).order_by("-date")[
                    :5
                ],
                "upcoming_events": Event.objects.filter(event_type="global").order_by(
                    "date"
                )[:5],
            }
        )

    # Group leader sees their groups events + sermons
    elif role == "leader":
        # assume user leades a group ; for simplicity, take first group
        # group_obj = getattr(user, "profile", None)
        group_obj = getattr(user.profile, "group", "")
        # group_obj = None
        # try:
        #     group_obj = user.profile.group_set.first()
        # except:
        #     pass

        context.update(
            {
                "group_events": (
                    Event.objects.filter(group=group_obj).order_by("date")[:5]
                    if group_obj
                    else []
                ),
                "group_sermons": (
                    Sermon.objects.filter(group=group_obj).order_by("-date")[:5]
                    if group_obj
                    else []
                ),
                "all_sermons": Sermon.objects.filter(group__isnull=True).order_by(
                    "-date"
                )[:5],
            }
        )

    # Member sees global events + sermons
    elif role == "member":
        context.update(
            {
                "upcoming_events": Event.objects.filter(event_type="global").order_by(
                    "date"
                )[:5],
                "latest_sermons": Sermon.objects.filter(group__isnull=True).order_by(
                    "-date"
                )[:5],
            }
        )

    return render(request, "dashboard/index.html", context)
