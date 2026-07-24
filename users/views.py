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
        return Task.objects.filter(user=self.request.user).select_related('user').prefetch_related('subtasks')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # type: ignore
        return SubTask.objects.filter(task__user=self.request.user).select_related('task')

    def perform_create(self, serializer):
        serializer.save()