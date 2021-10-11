
from django.urls import path,include

from notification.views import PendingNotifications


urlpatterns = [
    path('notification/',PendingNotifications.as_view(),name="notification")
    
]