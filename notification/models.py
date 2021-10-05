import uuid
from django.db import models
from django.db.models.deletion import CASCADE

from users.models import CustomUser
# Create your models here.


class ApproverNotification(models.Model):
    notifcation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    user = models.ForeignKey(
        CustomUser, on_delete=CASCADE, related_name="approver_notification")
    linkCreated = models.BooleanField(default=False)
    excelLink = models.URLField(null=True, blank=True)
    emailSend = models.BooleanField(default=False)
    workDone = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email+' | Email Sent: '+str(self.emailSend)+' | Workdone: '+str(self.workDone)
