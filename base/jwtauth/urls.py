from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterUserView, UserActivityList

urlpatterns = [
    path('user/register/', RegisterUserView.as_view(), name='register'),
    path('user/token/', TokenObtainPairView.as_view(), name='login'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    # since JWT is stateless, logout should be performed on the client-side by deleting stored jwt-token
    path('users/activity/', UserActivityList.as_view(), name='activity'),
]
