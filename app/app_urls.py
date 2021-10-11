from django.urls import path
from .views import *

urlpatterns = [
    path('openAPI/', OpenQuestionAPI.as_view(),name="Open Question"),
    path('openleadingAPI/', OpenLeadingQuestionAPI.as_view(),name="Open Leading Question"),
    path('closedAPI/', ClosedQuestionAPI.as_view(),name="Closed Question"),
]