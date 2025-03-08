from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DiaryEntry, UserProfile

@receiver(post_save, sender=DiaryEntry)
def update_user_profile(sender, instance, **kwargs):
    user_profile, created = UserProfile.objects.get_or_create(user=instance.user)
    user_profile.update_entries_count()