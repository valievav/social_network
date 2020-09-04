from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer


class PostListCreate(generics.ListCreateAPIView):
    """
    API endpoint to get all posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailRetrieve(generics.RetrieveAPIView):
    """
    API endpoint to get particular post details.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class LikePostCreateDestroy(generics.CreateAPIView):
    """
    API endpoint to like/unlike particular post.
    """
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Like.objects.filter(user=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError("You already liked this post.")

        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=user, post=post)
