from jsonfield import fields
from rest_framework import serializers
from .models import *

class IntensitySerializer(serializers.ModelSerializer):
    class Meta:
        model=Intensity
        fields=['answer']
        
class FeelingsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feelings
        fields=['answer','emotion']

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Emotion
        fields=["id","feelings"]
        
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model=Genre
        fields=['answer']

class DecadeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Decade
        fields=['answer']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=SubCategory
        fields=['answer']

class CategorySerializer(serializers.ModelSerializer):
    sub_category=SubCategorySerializer(read_only=True, many=True)
    class Meta:
        model=Category
        fields=('answer','sub_category')

class DummyListSerializer(serializers.ModelSerializer):
    class Meta:
        model=DummyList
        fields=('answer','subCategory','category','genre','decade')