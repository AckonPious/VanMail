from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User  

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ['username', 'email', 'location', 'is_active', 'is_admin', 'is_registry'] 
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('full_name', 'is_admin', 'is_registry')}), 
    )

    list_filter = ['is_active', 'is_staff', 'is_admin', 'is_registry']  

    search_fields = ['username', 'email', 'full_name']  

admin.site.register(User, UserAdmin)
