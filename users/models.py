from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['id']



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
    

