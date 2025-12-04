from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from groups.models import MinistryGroup


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(MinistryGroup, on_delete=models.CASCADE)
    date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=[("present", "Present"), ("absent", "Absent"), ("visitor", "Visitor")],
        default="present",
    )

    class Meta:
        unique_together = ("user", "group", "date")
