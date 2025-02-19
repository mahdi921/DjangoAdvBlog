from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Profile, User


# Signal to create a profile for a user when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
