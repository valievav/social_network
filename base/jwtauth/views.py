from django.contrib.auth import get_user_model
from .serializers import UserCreateSerializer
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registration_view(request):
    """
    API endpoint to register user with JWT.
    """
    serializer = UserCreateSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    data = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    return Response(data=data, status=status.HTTP_201_CREATED)
