from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from posts.models import Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def post_create(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post

    def get_queryset(self):
        post = self.post_create()
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        post = self.post_create()
        serializer.save(author=self.request.user, post=post)
