from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from .serializers import CreateUserSerializer


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny, )
