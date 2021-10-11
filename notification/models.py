import uuid
from django.db import models
from django.db.models.deletion import CASCADE
from django.dispatch import receiver
from django.db.models.signals import post_save
from users.models import CustomUser
# Create your models here.
from .utils import Util

class ApproverNotification(models.Model):
    notifcation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    user = models.ForeignKey(
        CustomUser, on_delete=CASCADE, related_name="approver_notification")

    excelLink = models.URLField(null=True, blank=True)
    emailSend = models.BooleanField(default=False)
    workDone = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email+' | Email Sent: '+str(self.emailSend)+' | Workdone: '+str(self.workDone)

@receiver(post_save, sender=ApproverNotification, dispatch_uid="send_email_notification")
def send_email(sender, instance, **kwargs):
    try:
        email_body = 'Hi ' + instance.user.username + ' You got a Question to approve click the link: \n' + instance.excelLink
        data = {'email_body': email_body, 'to_email': instance.user.email,'email_subject': 'Please Approve my Question', 'email_link': instance.excelLink}
        Util.send_email(data)
    except:
        pass