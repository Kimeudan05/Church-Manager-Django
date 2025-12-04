from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from groups.models import MinistryGroup
from sermons.models import Sermon
from events.models import Event


class AttendanceSheet(models.Model):
    ATTENDANCE_TYPES = (
        ("sermon", "Sermon"),
        ("event", "Event"),
        ("service", "Sunday Service"),
        ("fellowship", "Fellowship"),
    )

    date = models.DateField()
    type = models.CharField(max_length=20, choices=ATTENDANCE_TYPES)

    group = models.ForeignKey(
        MinistryGroup, on_delete=models.CASCADE, null=True, blank=True
    )

    # optional links
    sermon = models.ForeignKey(Sermon, on_delete=models.SET_NULL, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)

    recorded_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    total_present = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.get_type_display()} - {self.date}"


class AttendanceRecord(models.Model):
    attendance = models.ForeignKey(AttendanceSheet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.attendance.date} - {'Present' if self.present else 'Absent'}"
