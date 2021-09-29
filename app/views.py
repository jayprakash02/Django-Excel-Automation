from django.shortcuts import render
from rest_framework.response import Response

# Create your views here.
from rest_framework.views import APIView
from rest_framework import status

from users.models import CustomUser
from .models import *
from .semi_models import *
from .semi_model_serializers import *


class OpenLeadingQuestionAPI(APIView):
    pass


class OpenQuestionAPI(APIView):
    def get(self, request):
        intensity_Need = IntensitySerializer(
            Intensity.objects.filter(choice='Need'))
        intensity_Wish = IntensitySerializer(
            Intensity.objects.filter(choice='Wish'))
        intensity_Desire = IntensitySerializer(
            Intensity.objects.filter(choice='Desire'))
        intensity_Want = IntensitySerializer(
            Intensity.objects.filter(choice='Want'))
        
        intensity = {'Need': intensity_Need.data, 'Wish': intensity_Wish.data,
                     'Desire': intensity_Desire.data, 'Want': intensity_Want.data}

        feeling_Spirit = FeelingsSerializer(
            Feelings.objects.filter(choice='Spirit'))
        feeling_Profession = FeelingsSerializer(
            Feelings.objects.filter(choice='Profession'))
        feeling_Purpose = FeelingsSerializer(
            Feelings.objects.filter(choice='Purpose'))
        feeling_Reward = FeelingsSerializer(
            Feelings.objects.filter(choice='Reward'))
        
        feeling = {'Spirit': feeling_Spirit.data, 'Profession': feeling_Profession.data,
                   'Purpose': feeling_Purpose.data, 'Reward': feeling_Reward.data}

        question1 = 'Why would you do (this)?'
        question2 = 'When would you do (this)?'
        question3 = 'Who would you do (this)?'
        question4 = 'What would you like in return for doing (this)?'
        
        question = [question1, question2, question3, question4]

        data = {'Question': question,
                'Intensity': intensity, 'Feeling': feeling}

        return Response(data, status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        if self.request.data.__contains__("question_type") and self.request.data.__contains__("ID"):
            question_type = self.request.data["question_type"]
            user_id = self.request.data["question_type"]
            user_instance = CustomUser.objects.get(user_id=user_id)
            if question_type == 'LV':
                if self.request.data.__contains__("subject") and self.request.data.__contains__("tags") and self.request.data.__contains__("need") and self.request.data.__contains__("wish") and self.request.data.__contains__("desire") and self.request.data.__contains__("want"):
                    subject = self.request.data["subject"]
                    tags = self.request.data["tags"]
                    need = self.request.data["need"]
                    wish = self.request.data["wish"]
                    desire = self.request.data["desire"]
                    want = self.request.data["want"]
                    lf_instance = LifeVector.objects.create(
                        subject=subject, tags=tags, need=need, wish=wish, desire=desire, want=want)
                    lf_instance.save()
                    openquestion_instance = Qpen.objects.create(
                        question_type=question_type, user=user_instance, Lf=lf_instance)
                    openquestion_instance.save()
                return Response('Doesnt meet requirement for Life Vector', status=status.HTTP_400_BAD_REQUEST)
            elif question_type == 'LM':
                pass
        return Response('Question Type or ID is missing', status=status.HTTP_400_BAD_REQUEST)
