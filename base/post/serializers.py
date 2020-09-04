from rest_framework import serializers

from .models import Post, Like


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'url', 'title', 'body', 'author', 'created', 'last_modified', 'likes']

    def get_likes(self, post):
        return Like.objects.filter(post=post).count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id']
