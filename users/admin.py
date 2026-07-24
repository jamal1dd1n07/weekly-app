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


# 1. Task ichida SubTask'larni inline (ichma-ich) ko'rsatish uchun sinf:
class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1  # Yangi subtask qo'shish uchun 1 ta bo'sh qator
    fields = ['title', 'description', 'is_completed']  # 'completed' o'rniga 'is_completed'
    verbose_name = "SubTopshiriq"
    verbose_name_plural = "SubTopshiriqlar"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'is_completed', 'user']
    list_filter = ['is_completed', 'user']
    search_fields = ['title', 'description']
    
    # 2. SubTaskInline'ni bu yerga biriktiramiz:
    inlines = [SubTaskInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Barcha tasklarni chaqirib, baza so'rovlarini optimallashtiramiz (N+1 query muammosini oldini olish)
        return queryset.select_related('user').prefetch_related('subtasks')


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    # 3. 'completed' o'rniga 'is_completed' qilib bir xillashtirildi
    list_display = ['id', 'title', 'description', 'is_completed', 'task']
    list_filter = ['is_completed', 'task']
    search_fields = ['title', 'description']