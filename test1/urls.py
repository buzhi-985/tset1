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
from django.contrib.auth.models import User
from PetProfile.models import PetProfile as PetP
from ClerkProfile.models import ClerkPayroll
import PetProfile.views
from rest_framework import routers, serializers, viewsets




# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class PetProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PetP
        fields = '__all__'
        # fields = ['url', 'pet_name', 'pet_id', 'pet_age', 'user']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PetProfileViewSet(viewsets.ModelViewSet):
    queryset = PetP.objects.all()
    serializer_class = PetProfileSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'petprofile', PetProfileViewSet)

urlpatterns = [
    path('', PetProfile.views.profile),  # 默认首页为用户信息
    path('accounts/password/reset/', PetProfile.views.CustomPasswordResetView.as_view(), name="account_reset_password"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # 注册拓展的用户模型
    path('accounts/', include('PetProfile.urls')),
    path('bb/', PetProfile.views.bb),
    # 暴露api
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
