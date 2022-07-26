"""
Django settings for test1 project.

Generated by 'django-admin startproject' using Django 3.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.


BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-64azrxb^=g@i+(@($!9*jb9)%nca8v!rto^d(e**d_-rn298u5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
# Application definition
INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'PetProfile',
    # allauth依赖sites
    'django.contrib.sites',
    'django_apscheduler',
    # 导入allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'ClerkProfile',
    'rest_framework',
    'yuqing',


]
#rest鉴权方式
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        # 员工才可查看，添加两个鉴权时需要同时满足
        'rest_framework.permissions.IsAdminUser',
        # 'ClerkProfile.views.ClerkPermission'
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'test1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'test1.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DEFAULT_CHARSET = 'utf-8'
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # mysql 驱动
        'NAME': 'test1',  # 数据库名
        'USER': 'root',  # 用户名
        'PASSWORD': 'root',  # 密码
        'HOST': 'localhost',  # 访问的地址（localhost|127.0.0.1|''） 都代表本机
        # 'HOST': 'db',  # 服务器上填写docker db容器的名字
        'PORT': '3306',  # 端口号 mysql默认端口是3306
        'OPTIONS': {'charset': 'utf8mb4'},
    }

    # 'default': {
    #     'HOST': 'localhost',
    #     'PORT': 3306,
    #     'USER': 'root',
    #     'PASSWORD': 'root',
    #     'DB': 'test1',
    #     'ENGINE': pymysql.cursors.DictCursor
    # }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = False

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = 'yuqing/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# 文件上传功能
MEDIA_URL = '/appendix/'
# 设置上传文件的路径
MEDIA_ROOT = os.path.join(BASE_DIR, 'appendix')
# SITE_ID
SITE_ID = 1
# 使用邮箱或者username登录
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
# 是否需要邮箱
ACCOUNT_EMAIL_REQUIRED = True
# 指定授权
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
# accounts登录成功后跳转
LOGIN_REDIRECT_URL = '/accounts/profile/'
ACCOUNT_LOGOUT_ON_GET = True  # 用户登出(需要确认)
# allauth
ACCOUNT_EMAIL_VERIFICATION = 'none'  # 强制注册邮箱验证(注册成功后，会发送一封验证邮件，用户必须验证邮箱后，才能登陆)
# 将重写的form注册一下
ACCOUNT_FORMS = ({
    'signup': 'PetProfile.forms.CustomSignupForm',
    # 'reset_password': 'PetProfile.forms.CustomResetPasswordForm',
})
ACCOUNT_RESET_PASSWORD_FORM_CLASS = 'PetProfile.forms.CustomResetPasswordForm'  # 与上面的效果一样
# MEDIA_ROOT='appendix/'
EMAIL_FROM = "likebuzhi@qq.com"  # 发件人
# Host for sending email.
EMAIL_HOST = 'smtp.qq.com'  # 发送方的smtp服务器地址

# Port for sending email.
EMAIL_PORT = 587  # smtp服务端口

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = 'likebuzhi@qq.com'  # 发送方 邮箱地址
EMAIL_HOST_PASSWORD = 'leuhjrezwpxxcgaf'  # 获得的  授权码
EMAIL_USE_TLS = True  # 必须为True
EMAIL_USE_SSL = False
EMAIL_SSL_CERTFILE = None
EMAIL_SSL_KEYFILE = None
EMAIL_TIMEOUT = None

# Default email address to use for various automated correspondence from
# the site managers.
DEFAULT_FROM_EMAIL = 'likebuzhi@qq.com'  # 和 EMAIL_HOST_USER  相同
