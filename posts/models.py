from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL

class Post(models.Model):
    """Модель поста."""
    author = models.ForeignKey(User, verbose_name=_("Автор"), on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_("Текст"))
    image = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True,
        verbose_name=_("Фотография"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создан"))
    
    def __str__(self):
        return f'{self.author}: {self.text[:50]}...'

    class Meta:
        ordering = ["-created_at"]  # порядок сортировки по дате создания


class Comment(models.Model):
    """Модель комментария."""
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE, verbose_name=_("Пост"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Автор"))
    text = models.TextField(verbose_name=_("Текст"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создан"))
    
    def __str__(self):
        return f'{self.author}: {self.text[:50]}...'

    class Meta:
        ordering = ["-created_at"]  # порядок сортировки по дате создания


class Like(models.Model):
    """Модель лайка."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE, verbose_name=_("Пост"))

    class Meta:
        unique_together = ('user', 'post')  # уникальный лайк для каждого пользователя и поста
        
    def __str__(self):
        return f"{self.user} liked {self.post}"