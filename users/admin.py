from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Task, SubTask


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1  
    fields = ['title', 'description', 'is_completed']
    verbose_name = "Topshiriq"
    verbose_name_plural = "Topshiriqlar"


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    fieldsets = list(UserAdmin.fieldsets or []) + [
        ('Qo\'shimcha Ma\'lumotlar', {'fields': ('age', 'location', 'avatar', 'bio', 'time_zone', 'daily_goal_limit')}),
    ]
    
    add_fieldsets = list(UserAdmin.add_fieldsets or []) + [
        ('Qo\'shimcha Ma\'lumotlar', {'fields': ('age', 'location', 'avatar', 'bio', 'time_zone', 'daily_goal_limit')}),
    ]

    inlines = [TaskInline]
    
    list_display = ['id', 'username', 'email', 'age', 'is_staff', 'is_superuser', 'is_active']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'age', 'location']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'age', 'location']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('topshiriqlar')


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1 
    fields = ['title', 'description', 'is_completed']  
    verbose_name = "SubTopshiriq"
    verbose_name_plural = "SubTopshiriqlar"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'is_completed', 'user']
    list_filter = ['is_completed', 'user']
    search_fields = ['title', 'description']
    
    inlines = [SubTaskInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user').prefetch_related('subtasks')


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'is_completed', 'task']
    list_filter = ['is_completed', 'task']
    search_fields = ['title', 'description']