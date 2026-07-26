from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    # Qo'shimcha: foydalanuvchining nechta topshirig'i borligini hisoblash (Read-only)
    tasks_count = serializers.IntegerField(source='topshiriqlar.count', read_only=True)

    class Meta:
        model = MyUser
        fields = [
            'id', 
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'age', 
            'location', 
            'tasks_count',
            'date_joined',
            'avatar',
            'bio',
            'time_zone',
            'daily_goal_limit',
        ]
        # ID, username, email va ro'yxatdan o'tgan sanani o'zgartirib bo'lmaydigan qilamiz
        read_only_fields = ['id', 'username', 'email', 'date_joined']



class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'is_completed', 'task']
        read_only_fields = ['id', 'task']


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'user',
            'title',
            'description',
            'scheduled_date',
            'start_time',
            'end_time',
            'priority',
            'is_completed',
            'google_event_id',
            'calendar_sync_status',
            'subtasks',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'google_event_id', 'calendar_sync_status', 'subtasks']


class NotificationSerializer(serializers.ModelSerializer):
    """
    Bildirishnomalar uchun serializer.
    """
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'notification_type', 
            'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']