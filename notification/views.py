from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from notification.serializers import ANotificationSerializer

from users.models import CustomUser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PendingNotifications(APIView):
    user_id = openapi.Parameter(
        'user_id', in_=openapi.IN_QUERY, description='User ID', type=openapi.TYPE_STRING, required=True)
    
    @swagger_auto_schema(manual_parameters=[user_id])
    def get(self, request):
        if request.query_params["user_id"]:
            user_id = request.query_params["user_id"]
            user = get_object_or_404(CustomUser, user_id=user_id)
            notifiction = ANotificationSerializer(user.approver_notification.all(), many=True)
            return Response(notifiction.data,status=status.HTTP_202_ACCEPTED)
        return Response('user_id missing',status=status.HTTP_400_BAD_REQUEST)