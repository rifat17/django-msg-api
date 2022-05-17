from rest_framework import serializers, status

from django.contrib.auth import (
    get_user_model,
)

User = get_user_model()

from ..models import (
    MessagDBModel,
    MessageReqModel,
)

from apps.userauth.api.serializers import UserSerializer

class MessageReqModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageReqModel
        fields = '__all__'
        

class MessageDBModelSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    class Meta:
        model = MessagDBModel
        fields = '__all__'
        depth = 1
        

    def create(self, validated_data):
        # print(f"{self.created_by=}")
        return MessagDBModel.objects.create(**validated_data)
