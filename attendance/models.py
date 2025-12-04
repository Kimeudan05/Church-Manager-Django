from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from groups.models import MinistryGroup


class Attendance(models.Model):
    date = models.DateField()
    group = models.ForeignKey(
        MinistryGroup, on_delete=models.CASCADE, null=True, blank=True
    )
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    # summary fields (optional)
    total_present = models.IntegerField(default=0)

    def __str__(self):
        group_name = self.group.name if self.group else "All"
        return f"{group_name} - {self.date}"


class AttendanceRecord(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.attendance.date} - {'Present' if self.present else 'Absent'}"
