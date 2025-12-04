from django.db import models

from django.contrib.auth.models import User
from groups.models import MinistryGroup

# Create your models here.


class Profile(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("pastor", "Pastor"),
        ("leader", "Group Leader"),
        ("member", "Member"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="member")
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="profiles/", blank=True, null=True)

    # For group leaders and members (NR: Pastors/Admins can be in none)

    group = models.ForeignKey(
        MinistryGroup,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Only used for Group leaders & members",
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


# Reason:

# Group leaders belong to one ministry (Youth, KAMA, WCF, etc.)
# Members may also optionally belong to one group
# Admins & Pastors may not belong to any group
