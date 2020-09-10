from secrets import compare_digest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'}, label='confirm password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        password2 = validated_data['password2']

        if User.objects.filter(email=email).exclude(username=username).exists():
            raise serializers.ValidationError({'email': 'Already exists user with this email.'})

        if not compare_digest(password, password2):
            raise serializers.ValidationError({'password': 'Both passwords should be equal.'})

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    last_login = serializers.ReadOnlyField(source='user.last_login')

    class Meta:
        model = Profile
        fields = ('user_id', 'username', 'last_login', 'last_activity')
