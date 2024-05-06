from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render, redirect
from rest_framework_simplejwt.tokens import RefreshToken

from auth_.forms import UserCreationForm


  class RegistrationAPIView(APIView):

    def post(self, request):

        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            refresh = RefreshToken.for_user(user) 

            refresh.payload.update({   

                'user_id': user.id,

                'username': user.username

            })

            return Response({

                'refresh': str(refresh),

                'access': str(refresh.access_token),

            }, status=status.HTTP_201_CREATED)