import os
from urllib.parse import quote  # Для обработки специальных символов в URL
from rest_framework.reverse import reverse
from rest_framework import serializers
from django.conf import settings
from .models import Post, Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    """
    Серверизация модели комментария.
    Включает только авторство, текст и дату создания.
    """
    class Meta:
        model = Comment
        fields = ['author', 'text', 'created_at']
        read_only_fields = ['author', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    """
    Серверизация модели поста.
    Включает комментарии и количество лайков.
    """
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()  # Возвращает абсолютный путь изображения

    def get_image_url(self, obj):
        request = self.context.get('request')  # Берем объект запроса из контекста
        if obj.image:
            # Кодируем строку URL, если она содержит спецсимволы
            path = quote(obj.image.url)
            return request.build_absolute_uri(path)
        else:
            return None

    def get_likes_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Post
        fields = ["id", "text", "image_url", "created_at", "comments", "likes_count"]
        read_only_fields = ["created_at"]


class LikeSerializer(serializers.ModelSerializer):
    """
    Серверизация модели лайка.
    """
    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ['user', 'post']