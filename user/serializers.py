import logging
from django.contrib.auth import authenticate
from rest_framework import serializers
from user.models import User
from rest_framework.response import Response


logging.basicConfig(filename="user_serializer.log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'mobile_num', 'location',
                  'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            return User.objects.create_user(**validated_data)
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        try:
            user = authenticate(**data)
            if not user:
                raise serializers.ValidationError('Invalid Credentials')
            logger.info(f"User {data['username']} authenticated successfully.")
            return user  # Return the user object, not a dictionary
        except Exception as e:
            logger.error(f"Error during authentication: {e}")
            raise serializers.ValidationError({"error": str(e)})
