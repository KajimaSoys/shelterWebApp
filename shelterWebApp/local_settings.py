import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True
ALLOWED_HOSTS = []
SECRET_KEY = 'django-insecure-rq+vyc#d-r=hf)sere6_$02=n(np%k8&kw4+q)2xn1=zb@)uiu'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",# from nginx in prod
    "http://localhost:5173",# from vite in dev
    "http://localhost:4173"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shelter',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': 'D:/Programming/shelterWebApp/cache'
#     }
# }
