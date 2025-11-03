from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile
from django.contrib.auth import authenticate



class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(required=True)
    email= serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'phone', 'first_name', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        first_name = validated_data.pop('first_name')

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=first_name
        )

        Profile.objects.create(user=user, phone=phone)
        return user
  

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Find the user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "No user found with this email."})

        # DRF/Django’s default authenticate uses username, not email.
        user_auth = authenticate(username=user.username, password=password)
        if not user_auth:
            raise serializers.ValidationError({"password": "Invalid credentials."})

        attrs["user"] = user_auth
        return attrs