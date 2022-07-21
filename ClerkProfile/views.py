from django.shortcuts import render

# Create your views here.
from rest_framework import permissions


class ClerkPermission(permissions.IsAdminUser):
    def has_permission(self, request, view):
        clerk_staff = bool(request.user.last_name == 'staff')
        print(clerk_staff)
        return bool(request.user and clerk_staff)
