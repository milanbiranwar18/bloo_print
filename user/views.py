import logging
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer, LoginSerializer


logging.basicConfig(
    filename="user_activity.log",
    filemode='a',
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


@api_view(['POST'])
def user_registration(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info(f"User {request.data['username']} registered successfully.")
        return Response({'message': 'User registered successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    logger.error(f"User registration failed: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        logger.info(f"User {request.data['username']} logged in successfully.")
        return Response({
            'refresh token': str(refresh),
            'access token': str(refresh.access_token),
        })
    logger.error(f"User login failed: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_logout(request):
    try:
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()
        logger.info("User logged out successfully.")
        return Response({"message": "Logout successfully"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        logger.error(f"User logout failed: {e}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
