from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    time_zone = models.CharField(max_length=50, default='Asia/Tashkent')  
    daily_goal_limit = models.PositiveIntegerField(default=5)

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['id']

    def __str__(self):
        return self.username


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='topshiriqlar')
    scheduled_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    priority = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    google_event_id = models.CharField(max_length=255, null=True, blank=True)
    calendar_sync_status = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
            verbose_name = "Topshiriq"
            verbose_name_plural = "Topshiriqlar"
            ordering = ['id']
    


class SubTask(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')

    def __str__(self):
        return self.title


    class Meta:
            verbose_name = "SubTopshiriq"
            verbose_name_plural = "SubTopshiriqlar"
            ordering = ['id']
    


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        INFO = 'info', 'Info'
        WARNING = 'warning', 'Warning'
        TASK = 'task', 'Task Reminder'
        SYSTEM = 'system', 'System'

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20, 
        choices=NotificationType.choices, 
        default=NotificationType.INFO
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"