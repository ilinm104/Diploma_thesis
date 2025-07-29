from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    """
    Форма для создания нового поста.
    """
    class Meta:
        model = Post
        fields = ["text", "image"]  # Публикуемые поля: текст и фотография
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3}),  # Используем текстовую область
            "image": forms.ClearableFileInput(),       # Позволяет выбрать фотографию
        }

    def clean_image(self):
        """
        Проверяем правильность формата изображения.
        """
        image = self.cleaned_data.get("image")
        if not image:
            raise forms.ValidationError("Выберите изображение.")
        return image


class CommentForm(forms.ModelForm):
    """
    Форма для создания комментария.
    """
    class Meta:
        model = Comment
        fields = ["text"]  # Единственное публикуемое поле — текст комментария
        widgets = {"text": forms.Textarea(attrs={"rows": 3})}  # Текстовая область для ввода комментария