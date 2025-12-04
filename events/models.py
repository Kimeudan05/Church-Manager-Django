from django.db import models
from django.contrib.auth.models import User
from groups.models import MinistryGroup

from django.utils import timezone


# Create your models here.
class Event(models.Model):
    EVENT_TYPES = [
        ("global", "Church-wide"),
        ("group", "Group Only"),
        ("special", "Special Event"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()

    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default="global")
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    banner = models.ImageField(upload_to="events/", null=True, blank=True)

    group = models.ForeignKey(MinistryGroup, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
