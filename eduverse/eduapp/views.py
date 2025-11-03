from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.template.context_processors import request
from rest_framework import generics, status
from .serializers import RegisterSerializer,LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


def get_tokens_for_users(user):
   
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(APIView):
  

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        tokens = get_tokens_for_users(user)

        return Response(
            {"message": "Login successful", **tokens},
            status=status.HTTP_200_OK
        )