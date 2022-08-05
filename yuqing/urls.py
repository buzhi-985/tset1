from django.urls import path, include
from . import views

app_name = 'yuqing'

urlpatterns = [
    path("wei/", views.wei, name='wei'),
    path("msg", views.msg),
    path("msg/get/", views.msg_get),
    path("wei/ajax/", views.weiaj),
    path('wei/anly/',views.word_anlaies)
]
