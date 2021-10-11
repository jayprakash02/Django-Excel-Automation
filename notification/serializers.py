from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from rest_framework.utils import model_meta

from .models import *

class ANotificationSerializer(ModelSerializer):
    class Meta:
        model=ApproverNotification
        fields='__all__'