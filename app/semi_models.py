from typing import Callable
from django.db import models
from django.db.models.deletion import CASCADE
from jsonfield import JSONField

class Intensity(models.Model):
    Gradient=[('Need','Need'),('Wish','Wish'),('Desire','Desire'),('Want','Want')]
    answer=models.CharField(max_length=100)
    choice=models.CharField(choices=Gradient,max_length=10)

class Feelings(models.Model):
    Gradient=[('Spirit','Spirit'),('Profession','Profession'),('Purpose','Purpose'),('Reward','Reward')]
    answer=models.CharField(max_length=100)
    choice=models.CharField(choices=Gradient,max_length=10)

class Genre(models.Model):
    answer=models.CharField(max_length=100)

class Decade(models.Model):
    answer=models.CharField(max_length=100)

class Category(models.Model):
    answer=models.CharField(max_length=100)

class SubCategory(models.Model):
    answer=models.CharField(max_length=100)

class DummyList(models.Model):
    answer=models.CharField(max_length=100)
    subCategory=models.ForeignKey(SubCategory,on_delete=CASCADE,blank=True,null=True,related_name='dummylist_sub_c')
    category=models.ForeignKey(Category,on_delete=CASCADE,blank=True,null=True,related_name='dummylist_c')
    genre=models.ForeignKey(Genre,on_delete=CASCADE,blank=True,null=True,related_name='dummylist_genre')
    decade=models.ForeignKey(Decade,on_delete=CASCADE,blank=True,null=True,related_name='dummylist_decade')
