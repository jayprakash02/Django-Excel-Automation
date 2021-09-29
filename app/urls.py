from django.urls import path
from .views import *

urlpatterns = [
    path('openAPI/', OpenQuestionAPI.as_view,name="Open Question"),

]