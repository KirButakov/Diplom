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


class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    condition = models.CharField(max_length=100)  # Например, "5 записей"

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    entries_count = models.IntegerField(default=0)
    achievements = models.ManyToManyField(Achievement, blank=True)

    def __str__(self):
        return self.user.username

    def update_entries_count(self):
        self.entries_count = DiaryEntry.objects.filter(user=self.user).count()
        self.save()
        self.check_achievements()

    def check_achievements(self):
        achievements = Achievement.objects.all()
        for achievement in achievements:
            if self.entries_count >= int(achievement.condition):
                self.achievements.add(achievement)