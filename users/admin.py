from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser  

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


# Register your models here.
