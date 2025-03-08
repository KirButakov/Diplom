from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='diary_images/', null=True, blank=True)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title