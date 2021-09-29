from _typeshed import Self
from django.db.models import fields
from rest_framework import serializers
from .semi_models import *

class IntensitySerializer(serializers.ModelSerializer):
    class Meta:
        model=Intensity
        fields="__all__"

class FeelingsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feelings
        fields="__all__"
