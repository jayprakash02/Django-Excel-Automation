from typing import Callable
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from jsonfield import JSONField


class Intensity(models.Model):
    Gradient = [('Need', 'Need'), ('Wish', 'Wish'),
                ('Desire', 'Desire'), ('Want', 'Want')]
    answer = models.CharField(max_length=100)
    choice = models.CharField(choices=Gradient, max_length=10)

    def __str__(self):
        return self.answer


class Emotion(models.Model):
    Gradient = [('Spirit', 'Spirit'), ('Profession', 'Profession'),
                ('Purpose', 'Purpose'), ('Reward', 'Reward')]
    choice = models.CharField(choices=Gradient, max_length=10, null=True)
    feelings = models.CharField(max_length=50)

    def __str__(self):
        return self.feelings+' | '+self.choice


class Feelings(models.Model):
    Gradient = [('Spirit', 'Spirit'), ('Profession', 'Profession'),
                ('Purpose', 'Purpose'), ('Reward', 'Reward')]
    answer = models.CharField(max_length=100)
    emotion = models.ForeignKey(
        Emotion, null=True, blank=True, on_delete=CASCADE, related_name="feelings_emotion")
    choice = models.CharField(choices=Gradient, max_length=10)

    def __str__(self):
        return self.answer


class Genre(models.Model):
    answer = models.CharField(max_length=100)

    def __str__(self):
        return self.answer


class Decade(models.Model):
    answer = models.CharField(max_length=100)

    def __str__(self):
        return self.answer


class SubCategory(models.Model):
    answer = models.CharField(max_length=100)

    def __str__(self):
        return self.answer


class Category(models.Model):
    category_id = models.IntegerField(auto_created=True, primary_key=True)
    answer = models.CharField(max_length=100)
    sub_category = models.ManyToManyField(SubCategory, blank=True)

    def __str__(self):
        return self.answer


class QuestionTypeForDummy(models.Model):
    QUESTION_TYPE = [('Who', 'Who'), ('Which', 'Which'),
                     ('Where', 'Where'), ('When', 'When'), ('What', 'What')]
    question = models.CharField(
        choices=QUESTION_TYPE, max_length=5, default='Who')


class DummyList(models.Model):
    answer = models.CharField(max_length=100)
    question = models.ManyToManyField(
        QuestionTypeForDummy,  blank=True, related_name='dummylist_question',)
    category = models.ManyToManyField(
        Category,  blank=True, related_name='dummylist_c')
    genre = models.ManyToManyField(
        Genre, blank=True, related_name='dummylist_genre')
    decade = models.ManyToManyField(
        Decade, blank=True, related_name='dummylist_decade')
