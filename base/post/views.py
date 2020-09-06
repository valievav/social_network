from rest_framework import generics, status, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer


class PostListCreate(generics.ListCreateAPIView):
    """
    API endpoint to get all posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailRetrieve(generics.RetrieveAPIView):
    """
    API endpoint to get particular post details.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class LikePostCreateDestroy(generics.CreateAPIView, mixins.DestroyModelMixin):
    """
    API endpoint to like/unlike particular post.
    """
    serializer_class = LikeSerializer

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

    def delete(self, request, pk):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("You haven't liked this post.")
