from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group


class Users(AbstractUser):
    unique_code = models.CharField(
        max_length=36,
        null=True,
        blank=True,
        verbose_name='unique code',
    )
    chat_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='chat id',
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


@receiver(post_save, sender=Users)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        import uuid
        instance.unique_code = str(uuid.uuid4())
        instance.groups.add(
            Group.objects.get(name='customers'),
        )
        instance.save()
