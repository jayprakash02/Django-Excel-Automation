from django.db.models.signals import post_save
from django.dispatch import receiver


import pandas as pd
import numpy as np

from .models import *

@receiver(post_save, sender=Qpen, dispatch_uid="open_create_excel")
def create_excel(sender, instance, **kwargs):
    if instance.question_type=='LV':
        Lf=instance.Lf
        subject=Lf.subject
        sprit=['Why would you do {0}?'.format(subject),Lf.need[0],Lf.wish[0],Lf.desire[0],Lf.want[0]]
        profession=['When would you do {0}?'.format(subject),Lf.need[1],Lf.wish[1],Lf.desire[1],Lf.want[1]]
        purpose=['Who would you do {0}?'.format(subject),Lf.need[2],Lf.wish[2],Lf.desire[2],Lf.want[2]]
        reward=['What would you like in return for doing {0}?'.format(subject),Lf.need[3],Lf.wish[3],Lf.desire[3],Lf.want[3]]

        dict={'Sprit':sprit,'Profession':profession,'Purpose':purpose,'Reward':reward}
        df = pd.DataFrame(dict)
        df.to_excel("output.xlsx")

    elif instance.question_type=='LM':
        pass