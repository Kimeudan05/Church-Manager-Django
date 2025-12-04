from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MinistryGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ministry Group"
        verbose_name_plural = "Ministry Groups"


class GroupMembership(models.Model):
    group = models.ForeignKey(MinistryGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("group", "user")
