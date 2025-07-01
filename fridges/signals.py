from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Fridge

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_fridge_for_new_user(sender, instance, created, **kwargs):
    if created:
        Fridge.objects.create(user=instance)