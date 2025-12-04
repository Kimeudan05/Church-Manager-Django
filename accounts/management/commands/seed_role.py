from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = "Create default user roles for the church Manager"

    def handle(self, *args, **kwargs):
        roles = ["Admin", "Pastor", "GroupLeader", "Member"]

        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created {role} role"))
            else:
                self.stdout.write(self.style.WARNING(f"{role} role already exists"))
        self.stdout.write(self.style.SUCCESS(f"Role Setup Complete"))
