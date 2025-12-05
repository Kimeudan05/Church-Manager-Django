from django.db import models
from django.contrib.auth.models import User
from groups.models import MinistryGroup


# Create your models here.
class Sermon(models.Model):
    title = models.CharField(max_length=100)
    preacher = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )  # If you want a registered user
    # preacher = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()

    scripture = models.CharField(max_length=100, blank=True, null=True)

    pdf = models.FileField(upload_to="sermons/pdf/", blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to="sermons/thumbnails/", blank=True, null=True
    )

    group = models.ForeignKey(
        MinistryGroup, null=True, on_delete=models.SET_NULL, blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Sermon"
        verbose_name_plural = "Sermons"
