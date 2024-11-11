from django.db.models.signals import post_save
from django.dispatch import receiver
from mail.models import *  
from django.urls import reverse


# Signal when mail is set to "In Transit"
@receiver(post_save, sender=MailBox)
def notify_in_transit(sender, instance, created, **kwargs):
    if instance.mail_status == "In Transit":
        destination_location = instance.to_location
        message = f"Mailbag  {instance.mail_id} is in transit to {destination_location.name}."
        Notification.objects.create(location=destination_location, message=message)

# Signal when mail is set to "Received"
@receiver(post_save, sender=MailBox)
def notify_received(sender, instance, **kwargs):
    if instance.mail_status == "Received":
        origin_location = instance.from_location
        message = f"Mailbag  {instance.mail_id} has been received at {instance.to_location.name}."
        Notification.objects.create(location=origin_location, message=message)



