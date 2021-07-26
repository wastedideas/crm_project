from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from bot_notifier import bot


class Requests(models.Model):
    REPAIR = 're'
    SERVICE = 'se'
    CONSULTATION = 'co'
    REQUEST_TYPE = (
        (REPAIR, 'repair request'),
        (SERVICE, 'service request'),
        (CONSULTATION, 'consultation request'),
    )

    OPEN = 'op'
    CLOSE = 'cl'
    WORK = 'wo'
    REQUEST_STATUS = (
        (OPEN, 'open'),
        (CLOSE, 'close'),
        (WORK, 'at work'),
    )

    title = models.CharField(
        max_length=150,
        default='',
        null=False,
        verbose_name='title',
    )
    text = models.TextField(
        max_length=10000,
        default='',
        null=False,
        verbose_name='text',
    )
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='creation date',
    )
    request_type = models.CharField(
        max_length=2,
        choices=REQUEST_TYPE,
        default='',
        null=False,
        verbose_name='request type',
    )
    request_status = models.CharField(
        max_length=2,
        choices=REQUEST_STATUS,
        default='op',
        null=False,
        verbose_name='request status',
    )
    customer = models.ForeignKey(
        'app_users.Users',
        on_delete=models.CASCADE,
        verbose_name='customer',
        related_name='request',
    )
    worker = models.ForeignKey(
        'app_users.Users',
        on_delete=models.SET_DEFAULT,
        default='',
        null=True,
        blank=True,
        verbose_name='worker',
        related_name='request_to_work',
    )

    class Meta:
        verbose_name = 'request'
        verbose_name_plural = 'requests'
        permissions = [
            ('view_requests_list', 'Can view requests list')
        ]

    def __str__(self):
        return self.title

    @classmethod
    def status_changed(cls, new_entity):
        try:
            return (
                new_entity.request_status
                != Requests.objects.get(pk=new_entity.pk).request_status
            )
        except cls.DoesNotExist:
            return True


@receiver(pre_save, sender=Requests)
def notification_new_status(sender, instance, **kwargs):
    if Requests.status_changed(instance) and instance.customer.chat_id:
        status_changed_text_message = (
            'Hi, {user}! ✋\n'
            'Status of your request "{request}" has changed!\n'
            'It is *{new_status}* now!'
        ).format(
            user=instance.customer,
            request=instance,
            new_status=instance.get_request_status_display(),
        )
        bot.send_message(
            instance.customer.chat_id,
            status_changed_text_message,
            parse_mode='Markdown',
        )


@receiver(post_delete, sender=Requests)
def notification_delete_request(sender, instance, **kwargs):
    if instance.customer.chat_id:
        status_changed_text_message = (
            'Hi, {user}! ✋\n'
            'Status of your request "{request}" has changed!\n'
            'It is *delete* now!'
        ).format(
            user=instance.customer,
            request=instance,
        )
        bot.send_message(
            instance.customer.chat_id,
            status_changed_text_message,
            parse_mode='Markdown',
        )
