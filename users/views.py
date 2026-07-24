from django.views.generic import TemplateView
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # type: ignore
        # Faqat tizimga kirgan foydalanuvchining o'z vazifalarini qaytarish
        return Task.objects.filter(user=self.request.user).select_related('user')

    def perform_create(self, serializer):
        # Yangi task yaratilayotganda otomat ravishda joriy foydalanuvchini biriktirish
        serializer.save(user=self.request.user)