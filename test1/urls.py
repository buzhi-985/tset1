"""test1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

import PetProfile.views

urlpatterns = [
    path('', PetProfile.views.profile),# 默认首页为用户信息
    path('accounts/password/reset/',PetProfile.views.CustomPasswordResetView.as_view(),name="account_reset_password"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # 注册拓展的用户模型
    path('accounts/', include('PetProfile.urls')),
]
