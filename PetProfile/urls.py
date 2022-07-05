from django.urls import re_path, include
from . import views

app_name='PetProfile'

urlpatterns = [
    re_path(r'^profile/$', views.profile, name='profile'),
    re_path(r'^profile/update/$', views.profile_update, name='profile_update'),
]