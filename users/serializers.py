from rest_framework import serializers
from .models import *

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email', 'age', 'location']



class TaskSerializer(serializers.ModelSerializer):
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
            'parent_task', 
            'google_event_id', 
            'calendar_sync_status',
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'google_event_id', 'calendar_sync_status']



class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'completed', 'task']
