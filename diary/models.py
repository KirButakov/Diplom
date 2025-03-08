from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager


class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="diary_images/", null=True, blank=True)
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

    # Новый метод: получение следующего достижения
    def get_next_achievement(self):
        unlocked_achievements = self.achievements.all()
        all_achievements = Achievement.objects.all()
        next_achievement = None

        for achievement in all_achievements:
            if achievement not in unlocked_achievements:
                if not next_achievement or int(achievement.condition) < int(
                    next_achievement.condition
                ):
                    next_achievement = achievement

        return next_achievement

    # Новый метод: вычисление прогресса
    def get_progress(self):
        next_achievement = self.get_next_achievement()
        if next_achievement:
            progress = (self.entries_count / int(next_achievement.condition)) * 100
            return min(progress, 100)  # Ограничиваем прогресс 100%
        return 0
