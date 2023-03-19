from django.db import models
from django.conf import settings
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)
    open_profile = models.BooleanField(default=False)
    birthday = models.DateField()
    profile_photo = models.FileField()

    def __str__(self):
        return self.user.username


class Career(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)
    job = models.CharField(max_length=100)
    schools = models.JSONField()
    careers = models.JSONField()

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = RichTextUploadingField()
    tag = models.JSONField()
    published_date = models.DateTimeField(default=timezone.now)