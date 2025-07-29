import os
from pathlib import Path
from environ import Env

# Определение корневой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Создание экземпляра класса Env и чтение переменных окружения
env = Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

# Получение значений из переменных окружения
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])



# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",  # Включаем DRF для API
    "rest_framework.authtoken",  # Включаем механизм выдачи токенов
    "posts",  # Ваше собственное приложение
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "social_network.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "social_network.wsgi.application"

# Database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "social_network",  # Название базы данных
        "USER": "postgres",  # Пользователь базы данных
        "PASSWORD": "12viVI09",  # Пароль пользователя
        "HOST": "localhost",  # Адрес сервера базы данных
        "PORT": "5432",  # Порт базы данных
    }
}

# Authentication backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"  # URL для статичных ресурсов
STATICFILES_DIRS = [BASE_DIR / "static"]  # Директория для статических файлов

# Media files (загружаемые пользователем файлы)
MEDIA_URL = "/media/"  # URL для медиафайлов
MEDIA_ROOT = BASE_DIR / "media"  # Директория для загруженных файлов

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Конфигурация Django Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}

# Email setup (опционально)
EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"  # Логгирование почты в консоль
)