from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CreateUserView

urlpatterns = [
    path('user/register/', CreateUserView.as_view(), name='register'),
    path('user/token/', TokenObtainPairView.as_view(), name='login'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    # since JWT is stateless, logout should be performed on the client-side by deleting stored jwt-token
]
