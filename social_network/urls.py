from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts.views import PostViewSet, CommentViewSet, LikeViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)
router.register(r"likes", LikeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),  # Добавляем маршрут для административной панели
    path("", include(router.urls)),  # Регистрация роутов для API
]