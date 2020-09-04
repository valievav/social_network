from django.urls import path

from . import views

urlpatterns = [
    path('posts/', views.PostListCreate.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetailRetrieve.as_view(), name="post-detail"),
    path('posts/<int:pk>/like/', views.LikePostCreateDestroy.as_view(), name="like")
]
