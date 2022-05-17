from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .serializers import (
    UserRegisterSerializer, 
    UserLoginSerializer,
    UserSerializer,
    TokenSerializer
)


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = ((AllowAny,))

    def post(self, request):
        # print(f"{request.user=}")

        if not request.user.is_authenticated:
            user = request.data
            serializer = self.serializer_class(data=user)
            if serializer.is_valid():
                serializer.save()
                return Response(data={**serializer.data, "message": "Registration Successfull"}, status=status.HTTP_201_CREATED)
            else:   
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'Error': f'Already loggedin'}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(ObtainAuthToken):
    serializer_class = UserLoginSerializer
    permission_classes = ((AllowAny,))

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        try:
            if serializer.is_valid():
                # print(f"{serializer=}")
                user = serializer.validated_data
                token = Token.objects.get(user=user)

                return Response(data={
                    'token': token.key,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data={
                    'message': 'Unable to log in with provided credentials.'
                },status=status.HTTP_400_BAD_REQUEST)
        