from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Student


User = get_user_model()


@receiver(post_save, sender=User)
def create_student_for_user(sender, instance, created, **kwargs):
    if created:
        # create a Student linked to this User if not exists
        Student.objects.get_or_create(user=instance, defaults={'name': instance.username})
