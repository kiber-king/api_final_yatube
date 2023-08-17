from django.shortcuts import get_object_or_404

from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Group, Post

from .permissions import IsCreatorOrReadOnly
from .serializers import (CommentSerializers, FollowSerializers,
                          GroupSerializers, PostSerializers)


class PostViewSet(viewsets.ModelViewSet):
    """CRUD для постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializers
    pagination_class = LimitOffsetPagination
    permission_classes = (IsCreatorOrReadOnly,)

    def perform_create(self, serializer):
        """Функция для создания поста."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD для комментариев."""

    serializer_class = CommentSerializers
    permission_classes = (IsCreatorOrReadOnly,)

    def get_queryset(self):
        """Функция для получения комментариев заданного поста."""
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        return post.comments.all()

    def perform_create(self, serializer):
        """Функция для создания комментриев."""
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)


class FollowersViewSet(
    viewsets.ModelViewSet, mixins.CreateModelMixin, mixins.ListModelMixin
):
    """
    Вьюсет для показа всех подписок пользователя, который отправил запрос,
    и для оформления подписок.
    """

    serializer_class = FollowSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ("following__username",)

    def get_queryset(self):
        """Функция для получения подписок пользователя, совершившего запрос."""
        user = self.request.user
        return user.follower.all()

    def perform_create(self, serializer):
        """Функция для оформления подписки."""
        serializer.save(user=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для показа всех доступных групп."""

    serializer_class = GroupSerializers
    queryset = Group.objects.all()
    permission_classes = (IsCreatorOrReadOnly,)
