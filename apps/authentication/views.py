from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth.hashers import check_password
from drf_spectacular.utils import extend_schema
from datetime import datetime, timedelta, timezone

from ..user_management.models import User
from ..user_management.serializers import UserSerializer
from .serializers import LoginRequestSerializer
from ..generic_serializer import MessageResponseSerializer, ErrorResponseSerializer

@extend_schema(
    tags=['Auth'],
    request=UserSerializer,
    responses={201: UserSerializer, 400: ErrorResponseSerializer}
)
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags=['Auth'],
    request=LoginRequestSerializer,
    responses={200: MessageResponseSerializer, 401: ErrorResponseSerializer}
)
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, user.password):
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Create JWT token
        token = AccessToken.for_user(user)
        token['id'] = user.id

        response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='jwt',
            value=str(token),
            httponly=True,
            expires=datetime.now(timezone.utc) + timedelta(days=1)
        )
        return response

@extend_schema(
    tags=['Auth'],
    request=None,
    responses={200: MessageResponseSerializer}
)
class LogoutView(APIView):
    def post(self, request):
        response = Response({'message': 'Logged out'}, status=status.HTTP_200_OK)
        response.delete_cookie('jwt')
        return response

@extend_schema(
    tags=['Auth'],
    responses={200: UserSerializer, 401: ErrorResponseSerializer, 404: ErrorResponseSerializer}
)
class ProfileView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            access_token = AccessToken(token)
            user_id = access_token['id']
            user = User.objects.get(id=user_id)
        except (TokenError, InvalidToken):
            response = Response({'detail': 'Token expired or invalid. Please login again.'}, status=status.HTTP_401_UNAUTHORIZED)
            response.delete_cookie('jwt')
            return response
        except User.DoesNotExist:
            response = Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            response.delete_cookie('jwt')
            return response

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)