from typing import Callable
from django.db import models
from django.db.models.deletion import CASCADE
from jsonfield import JSONField

from users.models import CustomUser
# # Create your models here.
QuestionStyle=[('O','Open'),('OL','Open Leading'),('C','Closed')]


class Dummy(models.Model):
    question_type=models.CharField(max_length=10)
    category=models.CharField(max_length=10)
    decade=models.CharField(max_length=10)
    genre=models.CharField(max_length=10)
    word=models.CharField(max_length=10)
    selection=JSONField()

# class LearningMethod(models.Model):
#     sitution=models.CharField(max_length=300)
#     behaviour_values=JSONField(null=False)

class LifeVector(models.Model):
    subject= models.CharField(max_length=300)
    tags= JSONField(null=True)
    need= JSONField()
    wish= JSONField()
    desire= JSONField()
    want= JSONField()


class Qpen(models.Model):
    OpenQuestionType=[('LV','Life Vector'),('LM','Learning Method')]
    question_type=models.CharField(max_length=3,choices=OpenQuestionType)
    user=models.ForeignKey(CustomUser,on_delete=CASCADE,related_name="question",null=False)
    Lf=models.ForeignKey(LifeVector,null=True,blank=True,on_delete=CASCADE)
    # Lm=models.ForeignKey(LearningMethod,null=True,blank=True,on_delete=CASCADE)


#approver and creator are seperated

# class OpenLeading(models.Model):
#     OpenQuestionType=[('DU','Dummy'),('IDU','Inteligent Dummy')]
#     question_type=models.CharField(max_length=3,choices=OpenQuestionType)
#     user=models.ForeignKey(CustomUser,on_delete=CASCADE,related_name="question",null=False)
#     dummy=models.ForeignKey(Dummy,null=True,blank=True,on_delete=CASCADE)
#     # Inteligentdummy=models.ForeignKey(Dummy,null=True,blank=True,on_delete=CASCADE)

# class Closed(models.Model):
#     pass