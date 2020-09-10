from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView

from .models import Profile
from .serializers import RegisterUserSerializer
from .serializers import ProfileSerializer

User = get_user_model()


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = (permissions.AllowAny, )


class UserActivityList(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
