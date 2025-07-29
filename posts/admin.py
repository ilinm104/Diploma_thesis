from django.contrib import admin
from .models import Post, Comment, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Административная регистрация модели Пост"""
    list_display = ("id", "author", "text", "created_at")  # поля, отображаемые в списке
    search_fields = ("text", "author__username")           # поля для поиска
    readonly_fields = ("created_at", )                     # поля, доступные только для чтения
    list_filter = ("created_at", )                         # фильтры списка
    date_hierarchy = "created_at"                          # иерархический фильтр по датам
    autocomplete_fields = ("author", )                      # автозавершение выбора автора

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Административная регистрация модели Комментарий"""
    list_display = ("id", "post", "author", "text", "created_at")
    search_fields = ("text", "author__username")
    readonly_fields = ("created_at", )
    list_filter = ("created_at", )
    date_hierarchy = "created_at"
    autocomplete_fields = ("author", "post")

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Административная регистрация модели Лайк"""
    list_display = ("id", "user", "post")
    search_fields = ("user__username", "post__text")
    list_filter = ("user", "post")
    autocomplete_fields = ("user", "post")