from django.views.generic import TemplateView
from rest_framework import generics, mixins, status, permissions, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import *
from .serializers import *


from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .serializers import UserProfileSerializer

User = get_user_model()


class UserProfileView(APIView):
    """
    Tizimga kirgan foydalanuvchining o'z profilini ko'rishi (GET) 
    va tahrirlashi (PUT/PATCH) uchun APIView.
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser] 

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    
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


class NotificationViewSet(viewsets.ModelViewSet):
    """
    Bildirishnomalar bilan ishlash ViewSet'i.
    
    Faqat tizimga kirgan foydalanuvchining o'ziga tegishli
    bildirishnomalari bilan ishlashini ta'minlaydi.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self): # type: ignore
        # Faqat joriy foydalanuvchiga tegishli xabarnomalarni qaytaradi
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['patch'], url_path='read')
    def mark_as_read(self, request, pk=None):
        """
        PATCH /api/notifications/<id>/read/
        Bitta bildirishnomani 'o'qildi' (is_read=True) deb belgilash.
        """
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response(
            {'status': 'Notification marked as read'}, 
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'], url_path='read-all')
    def mark_all_as_read(self, request):
        """
        POST /api/notifications/read-all/
        Foydalanuvchining barcha o'qilmagan bildirishnomalarini 'o'qildi' qilish.
        """
        updated_count = self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response(
            {'status': f'{updated_count} notifications marked as read'}, 
            status=status.HTTP_200_OK
        )
