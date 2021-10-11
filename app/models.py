from django.shortcuts import get_object_or_404
from .credentials import creds
from googleapiclient import model
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from os import utime
from django.utils import tree
import numpy as np
import pandas as pd
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.db.models.deletion import CASCADE
from jsonfield import JSONField
from pyasn1.type.univ import Choice
import datetime

from users.models import CustomUser
# # Create your models here.
from .semi_models import *
from .utils import Util
# Open Leading - Inteligent Dummy(Life vector ,subject is to given by api)
# Closed - Dummy,Inteligent Dummy (Life vector ,subject is to given by api)


class Sheet(models.Model):
    QUESTION_TYPE = [('Life Vector', 'Life Vector'), ('Learning Method', 'Learning Method'),
                     ('Intelligent Dummy', 'Intelligent Dummy'), ('Dummy', 'Dummy')]
    question_type = models.CharField(choices=QUESTION_TYPE, max_length=20)
    sheetID = models.CharField(max_length=200)

    def __str__(self):
        return self.question_type


class Dummy(models.Model):
    question_type = models.CharField(max_length=10)
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100, null=True)
    decade = models.CharField(max_length=10)
    genre = models.CharField(max_length=10)
    word = models.CharField(max_length=10)
    selection1 = models.CharField(max_length=100, null=True)
    selection2 = models.CharField(max_length=100, null=True)
    answer=models.CharField(max_length=100, null=True)

# class LearningMethod(models.Model):
#     sitution=models.CharField(max_length=300)
#     behaviour_values=JSONField(null=False)


class LifeVector(models.Model):
    subject = models.CharField(max_length=300)
    situation = models.CharField(max_length=300, null=True)
    tags = JSONField(null=True)
    need = JSONField()
    wish = JSONField()
    desire = JSONField()
    want = JSONField()

    def __str__(self):
        return self.subject


class LearningMethod(models.Model):
    question = models.CharField(max_length=200)
    visual = models.CharField(max_length=50)
    auditory = models.CharField(max_length=50)
    kinetic = models.CharField(max_length=50)
    general = models.CharField(max_length=50)


class Qpen(models.Model):
    OpenQuestionType = [('LV', 'Life Vector'), ('LM', 'Learning Method')]
    question_type = models.CharField(max_length=3, choices=OpenQuestionType)
    Lf = models.ForeignKey(LifeVector, null=True,
                           blank=True, on_delete=CASCADE)
    Lm = models.ForeignKey(LearningMethod, null=True,
                           blank=True, on_delete=CASCADE)
    approver = models.ForeignKey(
        CustomUser, on_delete=CASCADE, related_name="open_approver", null=True)
    user = models.ForeignKey(
        CustomUser, on_delete=CASCADE, related_name="open_question", null=False)

    def __str__(self):
        if self.question_type == 'LV':
            return self.question_type+' | '+self.Lf.subject+' | '+self.user.email
        if self.question_type == 'LM':
            return self.question_type+' | '+self.Lm.question+' | '+self.user.email


class Closed(models.Model):
    ClosedQuestionType = [('DQ', 'Dummy Question'), ('ID', 'Inteligent Dummy')]
    question_type = models.CharField(max_length=3, choices=ClosedQuestionType)
    user = models.ForeignKey(
        CustomUser, on_delete=CASCADE, related_name="closed_question", null=False)
    IDummy = models.ForeignKey(
        LifeVector, null=True, blank=True, on_delete=CASCADE)
    Dummy = models.ForeignKey(Dummy, null=True, blank=True, on_delete=CASCADE)

    excelLink = models.URLField(blank=True, null=True)
    approverEmail = models.ForeignKey(
        CustomUser, on_delete=CASCADE, related_name="closed_approver", null=True)

    def __str__(self):
        if self.question_type == 'DQ':
            return self.question_type+' | '+self.Dummy.question_type+' | '+self.user.email
        if self.question_type == 'ID':
            return self.question_type+' | '+self.IDummy.subject+' | '+self.user.email


class OpenLeading(models.Model):
    OpenLeading = [('ID', 'Inteligent Dummy')]
    question_type = models.CharField(max_length=3, choices=OpenLeading)
    user = models.ForeignKey(
        CustomUser, on_delete=CASCADE, related_name="open_leading_question", null=False)
    IDummy = models.ForeignKey(
        LifeVector, null=True, blank=True, on_delete=CASCADE)

    excelLink = models.URLField(blank=True, null=True)
    approverEmail = models.ForeignKey(
        CustomUser, on_delete=CASCADE, related_name="openleading_approver", null=True)

    def __str__(self):
        if self.question_type == 'ID':
            return self.question_type+' | '+self.IDummy.subject+' | '+self.user.email


# authorize the clientsheet
service_excel = build('sheets', 'v4', credentials=creds)
service_drive = build('drive', 'v2', credentials=creds)

DEBUG = False


@receiver(post_save, sender=Qpen, dispatch_uid="open_create_excel")
def create_excel(sender, instance, **kwargs):
    if instance.question_type == 'LV':
        Lf = instance.Lf

        subject = Lf.subject
        situation = Lf.situation
        # sprit = ['When/If you are in {0},why would you {1}?'.format(situation,
        #                                                             subject), Lf.need["need"][0], Lf.wish["wish"][0], Lf.desire["desire"][0], Lf.want["want"][0]]
        # sprit_weight = [0, 8, 6, 4, 2]
        # profession = ['When/If you are in {0},when would you do {1}?'.format(situation,
        #                                                                      subject), Lf.need["need"][1], Lf.wish["wish"][1], Lf.desire["desire"][1], Lf.want["want"][1]]
        # profession_weight = [0, 2, 4, 6, 8]
        # purpose = ['When/If you are in {0},who would you do {1}?'.format(situation,
        #                                                                  subject), Lf.need["need"][2], Lf.wish["wish"][2], Lf.desire["desire"][2], Lf.want["want"][2]]
        # purpose_weight = [0, 8, 6, 4, 2]
        # reward = ['When/If you are in {0},what would you like in return for doing {1}?'.format(situation,
        #                                                                                        subject), Lf.need["need"][3], Lf.wish["wish"][3], Lf.desire["desire"][3], Lf.want["want"][3]]
        # reward_weight = [0, 2, 4, 6, 8]

        # dict = {'Sprit': sprit, 'w1': sprit_weight, 'Profession': profession, 'w2': profession_weight,
        #         'Purpose': purpose, 'w3': purpose_weight, 'Reward': reward, 'w4': reward_weight}
        # df = pd.DataFrame(dict)

        # filename = 'after_'+instance.question_type+'_Subject:' + \
        #     Lf.subject+'_Createdby:'+instance.user.email
        # Util.excel_sheet(service_excel=service_excel, service_drive=service_drive, data=df, title=filename,
        #                  approver_email=instance.approverEmail.email, admin_email=['unijay12@gmail.com'], question_type='LF')

        # filename = 'before_'+instance.question_type+'_Subject:' + \
        #     Lf.subject+'_Createdby:'+instance.user.email
        # Util.excel_sheet(service_excel=service_excel, service_drive=service_drive, data=df,
        #                  title=filename, approver_email='', admin_email=['unijay12@gmail.com'], question_type='LF')

        row = ["Open", str(datetime.datetime.now()), subject, situation, Lf.need["need"][0], Lf.need["need"][1], Lf.need["need"][2], Lf.need["need"][3], Lf.wish["wish"][0], Lf.wish["wish"][1], Lf.wish["wish"][2], Lf.wish["wish"][3], Lf.desire["desire"][0], Lf.desire["desire"][1], Lf.desire["desire"][2], Lf.desire["desire"][3], Lf.want["want"][0], Lf.want["want"][1], Lf.want["want"][2], Lf.want["want"][3], str(instance.user.user_id), str(instance.approver.user_id), "", "", "Open", str(
            datetime.datetime.now()), subject, situation, Lf.need["need"][0], Lf.need["need"][1], Lf.need["need"][2], Lf.need["need"][3], Lf.wish["wish"][0], Lf.wish["wish"][1], Lf.wish["wish"][2], Lf.wish["wish"][3], Lf.desire["desire"][0], Lf.desire["desire"][1], Lf.desire["desire"][2], Lf.desire["desire"][3], Lf.want["want"][0], Lf.want["want"][1], Lf.want["want"][2], Lf.want["want"][3], str(instance.user.user_id), str(instance.approver.user_id)]

        sheet_id = get_object_or_404(
            Sheet, question_type='Life Vector').sheetID
        Util.excel_sheet2(service_excel=service_excel,
                          row=row, sheet_id=sheet_id)

    elif instance.question_type == 'LM':
        lm = instance.Lm
        row = ["Open", str(datetime.datetime.now()), lm.question, lm.visual, lm.auditory, lm.kinetic, lm.general, str(instance.user.user_id), str(instance.approver.user_id), "", "", "Open", str(
            datetime.datetime.now()), lm.question, lm.visual, lm.auditory, lm.kinetic, lm.general, str(instance.user.user_id), str(instance.approver.user_id)]

        sheet_id = get_object_or_404(
            Sheet, question_type='Learning Method').sheetID
        Util.excel_sheet2(service_excel=service_excel,
                          row=row, sheet_id=sheet_id)


@receiver(post_save, sender=OpenLeading, dispatch_uid="open_leading_create_excel")
def create_excel(sender, instance, **kwargs):
    if instance.question_type == 'ID' and DEBUG:
        Lf = instance.IDummy

        subject = Lf.subject
        situation = Lf.situation
        # sprit = ['When/If you are in {0},why would you {1}?'.format(situation,
        #                                                             subject), Lf.need["need"][0], Lf.wish["wish"][0], Lf.desire["desire"][0], Lf.want["want"][0]]
        # sprit_weight = [0, 8, 6, 4, 2]
        # profession = ['When/If you are in {0},when would you do {1}?'.format(situation,
        #                                                                      subject), Lf.need["need"][1], Lf.wish["wish"][1], Lf.desire["desire"][1], Lf.want["want"][1]]
        # profession_weight = [0, 2, 4, 6, 8]
        # purpose = ['When/If you are in {0},who would you do {1}?'.format(situation,
        #                                                                  subject), Lf.need["need"][2], Lf.wish["wish"][2], Lf.desire["desire"][2], Lf.want["want"][2]]
        # purpose_weight = [0, 8, 6, 4, 2]
        # reward = ['When/If you are in {0},what would you like in return for doing {1}?'.format(situation,
        #                                                                                        subject), Lf.need["need"][3], Lf.wish["wish"][3], Lf.desire["desire"][3], Lf.want["want"][3]]
        # reward_weight = [0, 2, 4, 6, 8]

        # dict = {'Sprit': sprit, 'w1': sprit_weight, 'Profession': profession, 'w2': profession_weight,
        #         'Purpose': purpose, 'w3': purpose_weight, 'Reward': reward, 'w4': reward_weight}

        # df = pd.DataFrame(dict)

        # filename = 'after_'+instance.question_type+'_Subject:' + \
        #     Lf.subject+'_Createdby:'+instance.user.email
        # Util.excel_sheet(service_excel=service_excel, service_drive=service_drive, data=df, title=filename,
        #                  approver_email=instance.approverEmail.email, admin_email=['unijay12@gmail.com'], question_type='LF')

        # filename = 'before_'+instance.question_type+'_Subject:' + \
        #     Lf.subject+'_Createdby:'+instance.user.email
        # Util.excel_sheet(service_excel=service_excel, service_drive=service_drive, data=df,
        #                  title=filename, approver_email='', admin_email=['unijay12@gmail.com'], question_type='LF')

        row = ["Open", str(datetime.datetime.now()), subject, situation, Lf.need["need"][0], Lf.need["need"][1], Lf.need["need"][2], Lf.need["need"][3], Lf.wish["wish"][0], Lf.wish["wish"][1], Lf.wish["wish"][2], Lf.wish["wish"][3], Lf.desire["desire"][0], Lf.desire["desire"][1], Lf.desire["desire"][2], Lf.desire["desire"][3], Lf.want["want"][0], Lf.want["want"][1], Lf.want["want"][2], Lf.want["want"][3], str(instance.user.user_id), str(instance.approver.user_id), "", "", "Open", str(
            datetime.datetime.now()), subject, situation, Lf.need["need"][0], Lf.need["need"][1], Lf.need["need"][2], Lf.need["need"][3], Lf.wish["wish"][0], Lf.wish["wish"][1], Lf.wish["wish"][2], Lf.wish["wish"][3], Lf.desire["desire"][0], Lf.desire["desire"][1], Lf.desire["desire"][2], Lf.desire["desire"][3], Lf.want["want"][0], Lf.want["want"][1], Lf.want["want"][2], Lf.want["want"][3], str(instance.user.user_id), str(instance.approver.user_id)]

        sheet_id = get_object_or_404(
            Sheet, question_type='Learning Method').sheetID
        Util.excel_sheet2(service_excel=service_excel,
                          row=row, sheet_id=sheet_id)


@receiver(post_save, sender=Closed, dispatch_uid="closed_create_excel")
def create_excel(sender, instance, **kwargs):
    if instance.question_type == 'ID':
        Lf = instance.IDummy

        subject = Lf.subject
        situation = Lf.situation
        # sprit = ['When/If you are in {0},why would you {1}?'.format(situation,
        #                                                             subject), Lf.need["need"][0], Lf.wish["wish"][0], Lf.desire["desire"][0], Lf.want["want"][0]]
        # sprit_weight = [0, 8, 6, 4, 2]
        # profession = ['When/If you are in {0},when would you do {1}?'.format(situation,
        #                                                                      subject), Lf.need["need"][1], Lf.wish["wish"][1], Lf.desire["desire"][1], Lf.want["want"][1]]
        # profession_weight = [0, 2, 4, 6, 8]
        # purpose = ['When/If you are in {0},who would you do {1}?'.format(situation,
        #                                                                  subject), Lf.need["need"][2], Lf.wish["wish"][2], Lf.desire["desire"][2], Lf.want["want"][2]]
        # purpose_weight = [0, 8, 6, 4, 2]
        # reward = ['When/If you are in {0},what would you like in return for doing {1}?'.format(situation,
        #                                                                                        subject), Lf.need["need"][3], Lf.wish["wish"][3], Lf.desire["desire"][3], Lf.want["want"][3]]
        # reward_weight = [0, 2, 4, 6, 8]

        # dict = {'Sprit': sprit, 'w1': sprit_weight, 'Profession': profession, 'w2': profession_weight,
        #         'Purpose': purpose, 'w3': purpose_weight, 'Reward': reward, 'w4': reward_weight}

        # df = pd.DataFrame(dict)

        # filename = 'after_'+instance.question_type+'_Subject:' + \
        #     Lf.subject+'_Createdby:'+instance.user.email
        # Util.excel_sheet(service_excel=service_excel, service_drive=service_drive, data=df, title=filename,
        #                  approver_email=instance.approverEmail.email, admin_email=['unijay12@gmail.com'], question_type='LF')

        # filename = 'before_'+instance.question_type+'_Subject:' + \
        #     Lf.subject+'_Createdby:'+instance.user.email
        # Util.excel_sheet(service_excel=service_excel, service_drive=service_drive, data=df,
        #                  title=filename, approver_email='', admin_email=['unijay12@gmail.com'], question_type='LF')

        row = ["Open", str(datetime.datetime.now()), subject, situation, Lf.need["need"][0], Lf.need["need"][1], Lf.need["need"][2], Lf.need["need"][3], Lf.wish["wish"][0], Lf.wish["wish"][1], Lf.wish["wish"][2], Lf.wish["wish"][3], Lf.desire["desire"][0], Lf.desire["desire"][1], Lf.desire["desire"][2], Lf.desire["desire"][3], Lf.want["want"][0], Lf.want["want"][1], Lf.want["want"][2], Lf.want["want"][3], str(instance.user.user_id), str(instance.approver.user_id), "", "", "Open", str(
            datetime.datetime.now()), subject, situation, Lf.need["need"][0], Lf.need["need"][1], Lf.need["need"][2], Lf.need["need"][3], Lf.wish["wish"][0], Lf.wish["wish"][1], Lf.wish["wish"][2], Lf.wish["wish"][3], Lf.desire["desire"][0], Lf.desire["desire"][1], Lf.desire["desire"][2], Lf.desire["desire"][3], Lf.want["want"][0], Lf.want["want"][1], Lf.want["want"][2], Lf.want["want"][3], str(instance.user.user_id), str(instance.approver.user_id)]

        sheet_id = get_object_or_404(
            Sheet, question_type='Learning Method').sheetID
        Util.excel_sheet2(service_excel=service_excel,
                          row=row, sheet_id=sheet_id)

    elif instance.question_type == 'DQ':
        dummy = instance.Dummy
        # parameters = [dummy.question_type, dummy.category,
        #               dummy.sub_category, dummy.decade, dummy.genre, dummy.word]
        # name_parameters = ['Question Type', 'Category',
        #                    'Sub Category', 'Decade', 'Genre', 'Word']
        # question_string = dummy.question_type+' '+dummy.category+' by '+dummy.sub_category + \
        #     ' was the '+dummy.decade+' in ' + dummy.genre+' of the '+dummy.word
        # question = [str(question_string), '', '', '', '', '']
        # answer = [dummy.selection, '', '', '', '', '']

        # dict = {'': name_parameters, 'Input': parameters,
        #         'Question Formed': question, 'Answer Selected': answer}
        # df = pd.DataFrame(dict)

        # filename = 'after_'+instance.question_type+'_Createdby:'+instance.user.email
        # Util.excel_sheet(service_excel=service_excel, service_drive=service_drive, data=df, title=filename,
        #                  approver_email=instance.approverEmail.email, admin_email=['unijay12@gmail.com'], question_type='LF')

        # filename = 'before_'+instance.question_type+'_Createdby:'+instance.user.email
        # Util.excel_sheet(service_excel=service_excel, service_drive=service_drive, data=df,
        #                  title=filename, approver_email='', admin_email=['unijay12@gmail.com'], question_type='LF')

        row = ['Closed', str(datetime.datetime.now()), dummy.question_type, dummy.category, dummy.sub_category, dummy.decade, dummy.genre, dummy.word, dummy.selection, str(instance.user.user_id), str(instance.approverEmail.user_id), "", "", 'Closed', str(
            datetime.datetime.now()), dummy.question_type, dummy.category, dummy.sub_category, dummy.decade, dummy.genre, dummy.word, dummy.selection, str(instance.user.user_id), str(instance.approverEmail.user_id)]

        sheet_id = get_object_or_404(Sheet, question_type='Dummy').sheetID
        Util.excel_sheet2(service_excel=service_excel,
                          row=row, sheet_id=sheet_id)
