from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Task, SubTask

@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    # Pylance uchun eng xavfsiz usul: list ga o'tkazib qo'shish
    fieldsets = list(UserAdmin.fieldsets or []) + [
        ('Qo\'shimcha Ma\'lumotlar', {'fields': ('age', 'location')}),
    ]
    
    add_fieldsets = list(UserAdmin.add_fieldsets or []) + [
        ('Qo\'shimcha Ma\'lumotlar', {'fields': ('age', 'location')}),
    ]
    
    list_display = ['id', 'username', 'email', 'age', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'completed', 'user']
    list_filter = ['completed', 'user']
    search_fields = ['title', 'description']

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'completed', 'task']
    list_filter = ['completed', 'task']
    search_fields = ['title', 'description']
