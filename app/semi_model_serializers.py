from jsonfield import fields
from rest_framework import serializers
from .models import *


class IntensitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Intensity
        fields = ['answer']


class FeelingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feelings
        fields = ['answer', 'emotion']


class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ["id", "feelings"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['answer']


class DecadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decade
        fields = ['answer']


class QuestionTypeForDummySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTypeForDummy
        fields = ['question']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['answer']


class WordTypeForDummySerializer(serializers.ModelSerializer):
    class Meta:
        model = WordTypeForDummy
        fields = ['answer']


class CategorySerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ['answer', 'sub_category']


class DummyListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    genre = GenreSerializer(read_only=True, many=True)
    decade = DecadeSerializer(read_only=True, many=True)
    question = QuestionTypeForDummySerializer(read_only=True, many=True)
    word = WordTypeForDummySerializer(read_only=True, many=True)

    class Meta:
        model = DummyList
        fields = ['question', 'category', 'genre', 'decade', 'word']


class DummyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DummyList
        fields = ['answer']


class VisualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visual
        fields = ['answer']


class AuditorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditory
        fields = ['answer']


class KineticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kinetic
        fields = ['answer']


class GeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = General
        fields = ['answer']
