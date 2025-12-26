import os
import stat
import textwrap
import os
from django.core.asgi import get_asgi_application
import os
from django.core.wsgi import get_wsgi_application
from django.contrib import admin
from django.urls import path, include
import os
from pathlib import Path
import environ
import os
import sys
from django.core.management import execute_from_command_line
from django.apps import AppConfig
from django.db import models
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from django.test import TestCase
from django.urls import path
from . import views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from django.urls import path, include
from django.contrib import admin

# index.py
# Generator script to scaffold a professional Django project skeleton
# Run: python index.py
# Creates a "projeto_profissional" Django project structure in the current directory.


PROJECT_SLUG = "projeto_profissional"
DJANGO_PROJECT = "config"
APPS = ["users", "core", "products", "orders", "billing", "api"]
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

FILES = {
    ".gitignore": textwrap.dedent("""\
        __pycache__/
        *.py[cod]
        *.sqlite3
        env/
        .env
        .venv/
        *.log
        media/
        node_modules/
    """),
    "README.md": textwrap.dedent(f"""\
        # {PROJECT_SLUG}
        Professional Django project scaffold generated automatically.

        Structure highlights:
        - Django project: {DJANGO_PROJECT}
        - Apps: {', '.join(APPS)}
        - Docker, docker-compose, GitHub Actions, Celery, REST API ready
    """),
    "LICENSE": "MIT License\n\nCopyright (c) YEAR OWNER\n",
    "requirements.txt": textwrap.dedent("""\
        Django>=4.2
        djangorestframework
        psycopg2-binary
        gunicorn
        django-environ
        celery
        redis
        drf-yasg
        pytest
        pytest-django
    """),
    "Dockerfile": textwrap.dedent("""\
        FROM python:3.11-slim
        ENV PYTHONDONTWRITEBYTECODE 1
        ENV PYTHONUNBUFFERED 1
        WORKDIR /code
        COPY requirements.txt /code/
        RUN pip install --no-cache-dir -r requirements.txt
        COPY . /code/
        CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
    """),
    "docker-compose.yml": textwrap.dedent("""\
        version: '3.8'
        services:
          web:
            build: .
            command: bash -c "python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000"
            volumes:
              - .:/code
            ports:
              - "8000:8000"
            env_file:
              - .env
            depends_on:
              - db
              - redis
          db:
            image: postgres:15
            environment:
              POSTGRES_DB: django
              POSTGRES_USER: django
              POSTGRES_PASSWORD: django
            volumes:
              - postgres_data:/var/lib/postgresql/data/
          redis:
            image: redis:7
        volumes:
          postgres_data:
    """),
    ".env": textwrap.dedent("""\
        DEBUG=True
        SECRET_KEY=change-me
        DATABASE_URL=psql://django:django@db:5432/django
        REDIS_URL=redis://redis:6379/0
    """),
    ".github/workflows/django.yml": textwrap.dedent("""\
        name: Django CI

        on: [push, pull_request]

        jobs:
          test:
            runs-on: ubuntu-latest
            services:
              postgres:
                image: postgres:15
                env:
                  POSTGRES_DB: django
                  POSTGRES_USER: django
                  POSTGRES_PASSWORD: django
                ports:
                  - 5432:5432
                options: >-
                  --health-cmd pg_isready
                  --health-interval 10s
                  --health-timeout 5s
                  --health-retries 5
            steps:
              - uses: actions/checkout@v4
              - uses: actions/setup-python@v4
                with:
                  python-version: '3.11'
              - name: Install dependencies
                run: |
                  python -m pip install --upgrade pip
                  pip install -r requirements.txt
              - name: Run tests
                env:
                  DATABASE_URL: postgresql://django:django@localhost:5432/django
                run: pytest -q
    """),
}

# Django project files
FILES[f"{DJANGO_PROJECT}/__init__.py"] = ""
FILES[f"{DJANGO_PROJECT}/asgi.py"] = textwrap.dedent(f"""\

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{DJANGO_PROJECT}.settings")
    application = get_asgi_application()
""")

FILES[f"{DJANGO_PROJECT}/wsgi.py"] = textwrap.dedent(f"""\

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{DJANGO_PROJECT}.settings")
    application = get_wsgi_application()
""")

FILES[f"{DJANGO_PROJECT}/urls.py"] = textwrap.dedent("""\

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/', include('api.urls')),
    ]
""")

FILES[f"{DJANGO_PROJECT}/settings.py"] = textwrap.dedent(f"""\

    env = environ.Env()
    environ.Env.read_env(os.path.join(Path(__file__).resolve().parent.parent, '.env'))

    BASE_DIR = Path(__file__).resolve().parent.parent

    DEBUG = env.bool('DEBUG', default=False)
    SECRET_KEY = env('SECRET_KEY', default='change-me')
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'drf_yasg',
        'django_extensions',
        # local apps
        'users',
        'core',
        'products',
        'orders',
        'billing',
        'api',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = '{DJANGO_PROJECT}.urls'

    TEMPLATES = [
        {{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'],
            'APP_DIRS': True,
            'OPTIONS': {{
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            }},
        }},
    ]

    WSGI_APPLICATION = '{DJANGO_PROJECT}.wsgi.application'

    DATABASES = {{
        'default': env.db('DATABASE_URL', default='sqlite:///db.sqlite3')
    }}

    AUTH_PASSWORD_VALIDATORS = [
        {{
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        }},
        {{
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        }},
        {{
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        }},
        {{
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        }},
    ]

    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_TZ = True

    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    REST_FRAMEWORK = {{
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.BasicAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        ),
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
        'PAGE_SIZE': 20,
    }}

    # Celery
    CELERY_BROKER_URL = env('REDIS_URL', default='redis://localhost:6379/0')

    LOGGING = {{
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {{
            'console': {{
                'class': 'logging.StreamHandler',
            }},
        }},
        'root': {{
            'handlers': ['console'],
            'level': 'INFO',
        }},
    }}
""")

# manage.py
FILES["manage.py"] = textwrap.dedent(f"""\
    #!/usr/bin/env python

    def main():
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{DJANGO_PROJECT}.settings')
        try:
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django."
            ) from exc
        execute_from_command_line(sys.argv)

    if __name__ == '__main__':
        main()
""")

# Create app templates
for app in APPS:
    base = f"{app}"
    FILES[f"{base}/__init__.py"] = ""
    FILES[f"{base}/apps.py"] = textwrap.dedent(f"""\

        class {app.capitalize()}Config(AppConfig):
            default_auto_field = 'django.db.models.BigAutoField'
            name = '{app}'
    """)
    FILES[f"{base}/models.py"] = textwrap.dedent("""\

        class TimeStampedModel(models.Model):
            created_at = models.DateTimeField(auto_now_add=True)
            updated_at = models.DateTimeField(auto_now=True)

            class Meta:
                abstract = True
    """)
    FILES[f"{base}/admin.py"] = textwrap.dedent("""\
        # Register your models here.
    """)
    FILES[f"{base}/views.py"] = textwrap.dedent("""\

        def health(request):
            return HttpResponse('OK')
    """)
    FILES[f"{base}/tests.py"] = textwrap.dedent("""\

        class SanityTest(TestCase):
            def test_health(self):
                self.assertTrue(True)
    """)
    FILES[f"{base}/migrations/__init__.py"] = ""
    # for api app add serializers and urls
    if app == "api":
        FILES[f"{base}/urls.py"] = textwrap.dedent("""\

            urlpatterns = [
                path('health/', views.health, name='health'),
            ]
        """)
        FILES[f"{base}/views.py"] = textwrap.dedent("""\

            @api_view(['GET'])
            def health(request):
                return Response({'status': 'ok'})
        """)
        FILES[f"{base}/serializers.py"] = textwrap.dedent("""\
        """)

# core app with utils
FILES["core/__init__.py"] = ""
FILES["core/utils.py"] = textwrap.dedent("""\
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
""")

# simple urls at root to include admin and api
FILES["urls.py"] = textwrap.dedent("""\

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/', include('api.urls')),
    ]
""")

# Basic CI-friendly pytest.ini
FILES["pytest.ini"] = textwrap.dedent("""\
    [pytest]
    DJANGO_SETTINGS_MODULE = config.settings
    python_files = tests.py test_*.py *_tests.py
""")

def ensure_dirs(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    dirpath = os.path.dirname(path)
    if dirpath:
        ensure_dirs(dirpath)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    # make scripts executable if appropriate
    if path.endswith("manage.py"):
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)

def main():
    root = os.path.join(BASE_DIR, PROJECT_SLUG)
    if os.path.exists(root):
        print(f"Directory {root} already exists. Aborting.")
        return
    os.makedirs(root)
    for rel, content in FILES.items():
        full = os.path.join(root, rel)
        write_file(full, content)
    # create templates/static directories
    os.makedirs(os.path.join(root, "templates"), exist_ok=True)
    os.makedirs(os.path.join(root, "static"), exist_ok=True)
    print(f"Scaffold created at {root}")
    print("Next steps: create a virtualenv, install requirements, run 'python manage.py migrate' and 'python manage.py runserver' inside the project directory.")

if __name__ == "__main__":
    main()