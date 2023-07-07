"""
Django settings for game_server project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import asyncio
import pathlib
import sys
import uuid


VERSION = '0.1.17'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(uuid.uuid4())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'server_app',
    'users',
    'corsheaders',
    'channels'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:8080',
    'http://localhost:11000',
    'http://localhost:80',
    'http://localhost:443'
]

ROOT_URLCONF = 'ggj23.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ggj23.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
ENV_REF = os.environ.get('ENV_REF')
if ENV_REF == 'production':
    DATABASES = {
        'default': {
            'ENGINE': 'mysql.connector.django',
            'NAME': os.environ.get('MYSQL_DATABASE', ''),
            'USER': os.environ.get('MYSQL_USER', ''),
            'PASSWORD': os.environ.get('MYSQL_PASSWORD', ''),
            'HOST': os.environ.get('MYSQL_HOST', ''),
            'PORT': os.environ.get('MYSQL_PORT'),
            'OPTIONS': {
            'autocommit': True,
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_FINDERS = ["django.contrib.staticfiles.finders.AppDirectoriesFinder"]

CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
ASGI_APPLICATION = "ggj23.asgi.application"
GRAPHENE = {
    'SCHEMA': 'ggj23.schema.schema',
}


GQL_URL = os.environ.get('GQL_URL')

# GAME CONFIGS
GAME_CONFIG = {
    'MAX_LV': 100,
    'MAX_COPPER_COINS': 100,
    'MAX_SILVER_COINS': 100,
    'MAX_GOLD_COINS': 1000000,
    'SPAWN_RATE': .4,
    'MAX_ENEMIES_PER_AREA': 16
}

AMQP = {
    'hostname': os.environ.get('AMQP_HOST', ''),
    'userid': os.environ.get('AMQP_USER', ''),
    'password': os.environ.get('AMQP_PASSWORD', ''),
    'heartbeat': 4,
    'virtual_host': os.environ.get('AMQP_VHOST', '')
}
ROUTING_KEY = os.environ.get('ROUTING_KEY')
EXCHANGE_NAME = os.environ.get('EXCHANGE_NAME')
EXCHANGE_TYPE = os.environ.get('EXCHANGE_TYPE')
QUEUE = os.environ.get('QUEUE')
