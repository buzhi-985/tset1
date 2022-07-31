from django.urls import path, include
from . import views
urlpatterns = [
    path("wei/",views.weibo),
    path("msg/",views.msg),
    path("msg/get/",views.msg_get),
    ]