from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Create your views here.
from rest_framework.views import APIView
from rest_framework import status

from notification.models import ApproverNotification
from .serializer import LifeVectorSubjectSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from itertools import groupby

from users.models import CustomUser
from users.serializers import ApproverSerializer
from .models import *
from .semi_models import *
from .semi_model_serializers import *

from django.utils.datastructures import MultiValueDictKeyError


def groupby_emotion(data):
    def key_func(k): return k['emotion']
    res = []
    for k, g in groupby(sorted(data, key=key_func), key=key_func):
        obj = {'emotion': k,  'answer': []}
        for group in g:
            obj['answer'].append(group['answer'])
        res.append(obj)
    data = res
    return data


class ClosedQuestionAPI(APIView):
    question_type = openapi.Parameter(
        'question_type', in_=openapi.IN_QUERY, description='DQ or ID', type=openapi.TYPE_STRING, required=True)
    category_id = openapi.Parameter(
        'category_id', in_=openapi.IN_QUERY, description='Category ID to filter Sub category', type=openapi.TYPE_STRING, required=False)

    @swagger_auto_schema(manual_parameters=[question_type, category_id])
    def get(self, request):

        if request.query_params["question_type"]:

            user_data = ApproverSerializer(
                CustomUser.objects.filter(staff_type='A'), many=True)
            question_type = request.query_params["question_type"]
            if question_type == 'DQ':
                try:
                    category_id = request.query_params['category_id']
                    category = get_object_or_404(
                        Category, category_id=category_id)
                    sub_category = SubCategorySerializer(
                        category.category_belong.all())
                    return Response({'sub_category': sub_category}, status=status.HTTP_202_ACCEPTED)

                except MultiValueDictKeyError:
                    pass
                question = ['Who', 'Which', 'Where', 'When', 'What']
                category = CategorySerializer(
                    Category.objects.all(), many=True).data
                decade = DecadeSerializer(Decade.objects.all(), many=True).data
                genre = GenreSerializer(Genre.objects.all(), many=True).data
                word = ['best', 'worst', 'more intresting']
                data = {'Approver': user_data.data, 'question': question, 'category': category,
                        'decade': decade, 'genre': genre, 'word': word}
                return Response(data, status=status.HTTP_202_ACCEPTED)

            elif question_type == 'ID':
                subject = LifeVectorSubjectSerializer(
                    LifeVector.objects.all(), many=True)

                emotion_Spirit = EmotionSerializer(
                    Emotion.objects.filter(choice='Spirit'), many=True).data
                emotion_Profession = EmotionSerializer(
                    Emotion.objects.filter(choice='Profession'), many=True).data
                emotion_Purpose = EmotionSerializer(
                    Emotion.objects.filter(choice='Purpose'), many=True).data
                emotion_Reward = EmotionSerializer(
                    Emotion.objects.filter(choice='Reward'), many=True).data

                emotion = {"Spirit": emotion_Spirit, "Profession": emotion_Profession,
                           "Purpose": emotion_Purpose, "Reward": emotion_Reward}

                intensity_Need = IntensitySerializer(
                    Intensity.objects.filter(choice='Need'), many=True)
                intensity_Wish = IntensitySerializer(
                    Intensity.objects.filter(choice='Wish'), many=True)
                intensity_Desire = IntensitySerializer(
                    Intensity.objects.filter(choice='Desire'), many=True)
                intensity_Want = IntensitySerializer(
                    Intensity.objects.filter(choice='Want'), many=True)

                intensity = {'Need': intensity_Need.data, 'Wish': intensity_Wish.data,
                             'Desire': intensity_Desire.data, 'Want': intensity_Want.data}

                feeling_Spirit = FeelingsSerializer(
                    Feelings.objects.filter(choice='Spirit'), many=True).data
                feeling_Spirit = groupby_emotion(feeling_Spirit)

                feeling_Profession = FeelingsSerializer(
                    Feelings.objects.filter(choice='Profesesion'), many=True).data
                feeling_Profession = groupby_emotion(feeling_Profession)

                feeling_Purpose = FeelingsSerializer(
                    Feelings.objects.filter(choice='Purpose'), many=True).data
                feeling_Purpose = groupby_emotion(feeling_Purpose)

                feeling_Reward = FeelingsSerializer(
                    Feelings.objects.filter(choice='Reward'), many=True).data
                feeling_Reward = groupby_emotion(feeling_Reward)

                feeling = {'Spirit': feeling_Spirit, 'Profession': feeling_Profession,
                           'Purpose': feeling_Purpose, 'Reward': feeling_Reward}

                question1 = 'Why would you do (this)?'
                question2 = 'When would you do (this)?'
                question3 = 'Who would you do (this)?'
                question4 = 'What would you like in return for doing (this)?'

                question = [question1, question2, question3, question4]

                data = {'Approver': user_data.data, 'Subject': subject.data, 'Question': question, 'Emotion': emotion,
                        'Intensity': intensity, 'Feeling': feeling}

                return Response(data, status=status.HTTP_202_ACCEPTED)

            return Response('Question type not valid', status=status.HTTP_400_BAD_REQUEST)
        return Response('Pass Question type', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        if self.request.data.__contains__("question_type") and self.request.data.__contains__("ID") and self.request.data.__contains__("approver"):
            question_type = self.request.data["question_type"]
            user_id = self.request.data["ID"]
            user_instance = CustomUser.objects.get(user_id=user_id)
            approver_id = self.request.data["approver"]
            approver = get_object_or_404(CustomUser, user_id=approver_id)
            approver_instance = ApproverNotification.objects.create(user=approver)
            if question_type == 'ID':
                if self.request.data.__contains__("subject") and self.request.data.__contains__("situation") and self.request.data.__contains__("tags") and self.request.data.__contains__("need") and self.request.data.__contains__("wish") and self.request.data.__contains__("desire") and self.request.data.__contains__("want"):
                    subject = self.request.data["subject"]
                    tags = self.request.data["tags"]
                    need = self.request.data["need"]
                    wish = self.request.data["wish"]
                    desire = self.request.data["desire"]
                    want = self.request.data["want"]
                    situation = self.request.data["situation"]
                    lf_instance = LifeVector.objects.create(
                        subject=subject, tags=tags, need=need, situation=situation, wish=wish, desire=desire, want=want)
                    lf_instance.save()
                    question_instance = Closed.objects.create(
                        question_type=question_type, user=user_instance,approverEmail=approver ,IDummy=lf_instance)
                    question_instance.save()
                    approver_instance.excelLink = question_instance.excelLink
                    approver_instance.linkCreated = True
                    approver_instance.save()
                    return Response(status=status.HTTP_202_ACCEPTED)
                return Response('Doesnt meet requirement for Inteligent Dummy', status=status.HTTP_400_BAD_REQUEST)
            elif question_type == 'DQ':
                if self.request.data.__contains__("question") and self.request.data.__contains__("category") and self.request.data.__contains__("sub_category") and self.request.data.__contains__("decade") and self.request.data.__contains__("genre") and self.request.data.__contains__("word") and self.request.data.__contains__("selection"):
                    question = self.request.data['question']
                    category = self.request.data['category']
                    sub_category = self.request.data['sub_category']
                    decade = self.request.data['decade']
                    genre = self.request.data['genre']
                    word = self.request.data['word']
                    selection = self.request.data['selection']
                    dummy_intance = Dummy.objects.create(
                        question_type=question, category=category, sub_category=sub_category, decade=decade, genre=genre, word=word, selection=selection)
                    dummy_intance.save()
                    question_instance = Closed.objects.create(
                        question_type=question_type, user=user_instance,approverEmail=approver ,Dummy=dummy_intance)
                    question_instance.save()
                    return Response(status=status.HTTP_202_ACCEPTED)
                return Response('Doesnt meet requirement for Dummy Question', status=status.HTTP_400_BAD_REQUEST)
        return Response('Question Type or ID is missing', status=status.HTTP_400_BAD_REQUEST)


class OpenLeadingQuestionAPI(APIView):
    def get(self, request):
        user_data = ApproverSerializer(
            CustomUser.objects.filter(staff_type='A'), many=True)

        subject = LifeVectorSubjectSerializer(
            LifeVector.objects.all(), many=True)

        emotion_Spirit = EmotionSerializer(
            Emotion.objects.filter(choice='Spirit'), many=True).data
        emotion_Profession = EmotionSerializer(
            Emotion.objects.filter(choice='Profession'), many=True).data
        emotion_Purpose = EmotionSerializer(
            Emotion.objects.filter(choice='Purpose'), many=True).data
        emotion_Reward = EmotionSerializer(
            Emotion.objects.filter(choice='Reward'), many=True).data

        emotion = {"Spirit": emotion_Spirit, "Profession": emotion_Profession,
                   "Purpose": emotion_Purpose, "Reward": emotion_Reward}

        intensity_Need = IntensitySerializer(
            Intensity.objects.filter(choice='Need'), many=True)
        intensity_Wish = IntensitySerializer(
            Intensity.objects.filter(choice='Wish'), many=True)
        intensity_Desire = IntensitySerializer(
            Intensity.objects.filter(choice='Desire'), many=True)
        intensity_Want = IntensitySerializer(
            Intensity.objects.filter(choice='Want'), many=True)

        intensity = {'Need': intensity_Need.data, 'Wish': intensity_Wish.data,
                     'Desire': intensity_Desire.data, 'Want': intensity_Want.data}

        feeling_Spirit = FeelingsSerializer(
            Feelings.objects.filter(choice='Spirit'), many=True).data
        feeling_Spirit = groupby_emotion(feeling_Spirit)

        feeling_Profession = FeelingsSerializer(
            Feelings.objects.filter(choice='Profesesion'), many=True).data
        feeling_Profession = groupby_emotion(feeling_Profession)

        feeling_Purpose = FeelingsSerializer(
            Feelings.objects.filter(choice='Purpose'), many=True).data
        feeling_Purpose = groupby_emotion(feeling_Purpose)

        feeling_Reward = FeelingsSerializer(
            Feelings.objects.filter(choice='Reward'), many=True).data
        feeling_Reward = groupby_emotion(feeling_Reward)

        feeling = {'Spirit': feeling_Spirit, 'Profession': feeling_Profession,
                   'Purpose': feeling_Purpose, 'Reward': feeling_Reward}

        question1 = 'Why would you do (this)?'
        question2 = 'When would you do (this)?'
        question3 = 'Who would you do (this)?'
        question4 = 'What would you like in return for doing (this)?'

        question = [question1, question2, question3, question4]

        data = {'Approver': user_data.data, 'Subject': subject.data, 'Question': question, 'Emotion': emotion,
                'Intensity': intensity, 'Feeling': feeling}

        return Response(data, status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        if self.request.data.__contains__("question_type") and self.request.data.__contains__("ID") and self.request.data.__contains__("approver"):
            question_type = self.request.data["question_type"]
            user_id = self.request.data["ID"]
            user_instance = CustomUser.objects.get(user_id=user_id)
            approver_id = self.request.data["approver"]
            approver = get_object_or_404(CustomUser, user_id=approver_id)
            approver_instance = ApproverNotification.objects.create(user=approver)
            if question_type == 'ID':
                if self.request.data.__contains__("subject") and self.request.data.__contains__("situation") and self.request.data.__contains__("tags") and self.request.data.__contains__("need") and self.request.data.__contains__("wish") and self.request.data.__contains__("desire") and self.request.data.__contains__("want"):
                    subject = self.request.data["subject"]
                    tags = self.request.data["tags"]
                    need = self.request.data["need"]
                    wish = self.request.data["wish"]
                    desire = self.request.data["desire"]
                    want = self.request.data["want"]
                    situation = self.request.data["situation"]
                    lf_instance = LifeVector.objects.create(
                        subject=subject, tags=tags, need=need, situation=situation, wish=wish, desire=desire, want=want)
                    lf_instance.save()
                    question_instance = OpenLeading.objects.create(
                        question_type=question_type, user=user_instance,approverEmail=approver ,IDummy=lf_instance)
                    question_instance.save()
                    approver_instance.excelLink = question_instance.excelLink
                    approver_instance.linkCreated = True
                    approver_instance.save()
                    return Response(status=status.HTTP_202_ACCEPTED)
                return Response('Doesnt meet requirement for Intelligent Dummy', status=status.HTTP_400_BAD_REQUEST)
            elif question_type == 'LM':
                pass
        return Response('Question Type or ID is missing', status=status.HTTP_400_BAD_REQUEST)


class OpenQuestionAPI(APIView):
    def get(self, request):
        user_data = ApproverSerializer(
            CustomUser.objects.filter(staff_type='A'), many=True)

        emotion_Spirit = EmotionSerializer(
            Emotion.objects.filter(choice='Spirit'), many=True).data
        emotion_Profession = EmotionSerializer(
            Emotion.objects.filter(choice='Profession'), many=True).data
        emotion_Purpose = EmotionSerializer(
            Emotion.objects.filter(choice='Purpose'), many=True).data
        emotion_Reward = EmotionSerializer(
            Emotion.objects.filter(choice='Reward'), many=True).data

        emotion = {"Spirit": emotion_Spirit, "Profession": emotion_Profession,
                   "Purpose": emotion_Purpose, "Reward": emotion_Reward}

        intensity_Need = IntensitySerializer(
            Intensity.objects.filter(choice='Need'), many=True)
        intensity_Wish = IntensitySerializer(
            Intensity.objects.filter(choice='Wish'), many=True)
        intensity_Desire = IntensitySerializer(
            Intensity.objects.filter(choice='Desire'), many=True)
        intensity_Want = IntensitySerializer(
            Intensity.objects.filter(choice='Want'), many=True)

        intensity = {'Need': intensity_Need.data, 'Wish': intensity_Wish.data,
                     'Desire': intensity_Desire.data, 'Want': intensity_Want.data}

        feeling_Spirit = FeelingsSerializer(
            Feelings.objects.filter(choice='Spirit'), many=True).data
        feeling_Spirit = groupby_emotion(feeling_Spirit)

        feeling_Profession = FeelingsSerializer(
            Feelings.objects.filter(choice='Profesesion'), many=True).data
        feeling_Profession = groupby_emotion(feeling_Profession)

        feeling_Purpose = FeelingsSerializer(
            Feelings.objects.filter(choice='Purpose'), many=True).data
        feeling_Purpose = groupby_emotion(feeling_Purpose)

        feeling_Reward = FeelingsSerializer(
            Feelings.objects.filter(choice='Reward'), many=True).data
        feeling_Reward = groupby_emotion(feeling_Reward)

        feeling = {'Spirit': feeling_Spirit, 'Profession': feeling_Profession,
                   'Purpose': feeling_Purpose, 'Reward': feeling_Reward}

        question1 = 'Why would you do (this)?'
        question2 = 'When would you do (this)?'
        question3 = 'Who would you do (this)?'
        question4 = 'What would you like in return for doing (this)?'

        question = [question1, question2, question3, question4]

        data = {'Approver': user_data.data, 'Question': question, 'Emotion': emotion,
                'Intensity': intensity, 'Feeling': feeling}

        return Response(data, status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        if self.request.data.__contains__("question_type") and self.request.data.__contains__("ID") and self.request.data.__contains__("approver"):
            question_type = self.request.data["question_type"]
            user_id = self.request.data["ID"]
            user_instance = CustomUser.objects.get(user_id=user_id)
            approver_id = self.request.data["approver"]
            approver = get_object_or_404(CustomUser, user_id=approver_id)
            approver_instance = ApproverNotification.objects.create(user=approver)
            if question_type == 'LV':
                if self.request.data.__contains__("subject") and self.request.data.__contains__("situation") and self.request.data.__contains__("tags") and self.request.data.__contains__("need") and self.request.data.__contains__("wish") and self.request.data.__contains__("desire") and self.request.data.__contains__("want"):
                    subject = self.request.data["subject"]
                    tags = self.request.data["tags"]
                    need = self.request.data["need"]
                    wish = self.request.data["wish"]
                    desire = self.request.data["desire"]
                    want = self.request.data["want"]
                    situation = self.request.data["situation"]
                    lf_instance = LifeVector.objects.create(
                        subject=subject, tags=tags, need=need, situation=situation, wish=wish, desire=desire, want=want)
                    lf_instance.save()
                    openquestion_instance = Qpen.objects.create(
                        question_type=question_type, user=user_instance,approverEmail=approver ,Lf=lf_instance)
                    openquestion_instance.save()
                    approver_instance.excelLink = openquestion_instance.excelLink
                    approver_instance.linkCreated = True
                    approver_instance.save()
                    return Response(status=status.HTTP_202_ACCEPTED)
                return Response('Doesnt meet requirement for Life Vector', status=status.HTTP_400_BAD_REQUEST)
            elif question_type == 'LM':
                pass
        return Response('Question Type or ID is missing', status=status.HTTP_400_BAD_REQUEST)
