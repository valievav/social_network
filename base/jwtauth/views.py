from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView

from .models import Profile
from .serializers import CreateUserSerializer
from .serializers import ProfileSerializer

User = get_user_model()


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny, )
