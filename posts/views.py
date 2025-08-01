from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from django.utils.translation import gettext_lazy as _

# Обработчик для просмотра списка и отдельных записей постов
class PostViewSet(viewsets.ModelViewSet):
    """
    Представление для управления постами.
    Доступно только авторизованным пользователям.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Сохраняем нового автора поста автоматически
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        # Извлекаем экземпляр поста
        instance = self.get_object()
        # Проверяем, совпадает ли автор поста с текущим пользователем
        if instance.author != request.user:
            return Response({'error': _('Вы не можете редактировать чужой пост.')}, status=status.HTTP_403_FORBIDDEN)
        # Если автор совпал, продолжаем операцию обновления
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # Извлекаем экземпляр поста
        instance = self.get_object()
        # Проверяем, совпадает ли автор поста с текущим пользователем
        if instance.author != request.user:
            return Response({'error': _('Вы не можете удалять чужой пост.')}, status=status.HTTP_403_FORBIDDEN)
        # Удаляем пост
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# Обработчик для просмотра списка и отдельных записей комментариев
class CommentViewSet(viewsets.ModelViewSet):
    """
    Представление для управления комментариями.
    Доступно только авторизованным пользователям.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Автоматически сохраняем автора комментария
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        # Извлекаем экземпляр комментария
        instance = self.get_object()
        # Проверяем, совпадает ли автор комментария с текущим пользователем
        if instance.author != request.user:
            return Response({'error': _('Вы не можете редактировать чужой комментарий.')}, status=status.HTTP_403_FORBIDDEN)
        # Продолжаем операцию обновления
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # Извлекаем экземпляр комментария
        instance = self.get_object()
        # Проверяем, совпадает ли автор комментария с текущим пользователем
        if instance.author != request.user:
            return Response({'error': _('Вы не можете удалять чужой комментарий.')}, status=status.HTTP_403_FORBIDDEN)
        # Удаляем комментарий
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# Обработчик для лайков
class LikeViewSet(viewsets.ModelViewSet):
    """
    Представление для управления лайками.
    Доступно только авторизованным пользователям.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Создаем новый лайк, связывая его с текущим пользователем
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Проверяем, существует ли уже лайк от этого пользователя для данного поста
        try:
            like = Like.objects.get(user=request.user, post_id=request.data.get('post'))
            return Response({'error': _('Вы уже поставили лайк этому посту.')}, status=status.HTTP_400_BAD_REQUEST)
        except Like.DoesNotExist:
            pass
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        # Возврат всего набора лайков без фильтров
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # Извлекаем экземпляр лайка
        instance = self.get_object()
        # Проверяем, принадлежит ли лайк текущему пользователю
        if instance.user != request.user:
            return Response({'error': _('Вы не можете удалять чужой лайк.')}, status=status.HTTP_403_FORBIDDEN)
        # Уничтожаем лайк
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)