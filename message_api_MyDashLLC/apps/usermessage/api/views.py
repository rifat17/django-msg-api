from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from datetime import datetime, timedelta
from django.utils import timezone
from ..models import MessagDBModel
from .serializers import (
    MessageDBModelSerializer,
    MessageReqModelSerializer,
)

class MessageApiView(generics.CreateAPIView):
    serializer_class = MessageReqModelSerializer
    db_model_class = MessagDBModel
    db_model_serializer = MessageDBModelSerializer
    permission_classes = (IsAuthenticated,)
    TIME_THRESHOLD = 1

    def post(self, request):
        user = request.user
        now = timezone.now()

        one_sec_ago = now - timedelta(seconds=1) # there might have a healthy argument!
        time_threshold = now - timedelta(hours=self.TIME_THRESHOLD)

        msgs_in_threshold = self.db_model_class.objects.filter(
            created_by=user,
            created_at__range=(time_threshold, one_sec_ago)
        )

        msg_aged_gt_threshold = self.db_model_class.objects.filter(
            created_by=user,
            created_at__lt=time_threshold
        )
        # we may delete old msgs
        # we may attach time_threshold to user model then user specific different threshold may apply 

        # print(f"{len(msgs_in_threshold)=}")
        if len(msgs_in_threshold) < 10:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                msg_data = serializer.data
                newData = self.db_model_class(created_by=user, **msg_data)
                newData.save()
                serializer = self.db_model_serializer(newData)
                return Response(data={
                            'data': serializer.data,
                        }, status=status.HTTP_200_OK)
            else:
                return Response(data={
                    'error': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(data={
                    'error': f'{self.TIME_THRESHOLD} hour Msg Quota Complete'
                    }, status=status.HTTP_403_FORBIDDEN
                )
        