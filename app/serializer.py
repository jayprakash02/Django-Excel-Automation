from django.db.models import fields
from .models import * 
from rest_framework import serializers

class LifeVectorSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=LifeVector
        fields=['subject']