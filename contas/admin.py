from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ResellerUser

@admin.register(ResellerUser)
class ResellerUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password')}),
        ('Informações pessoais', {'fields': ('full_name',)}),
        ('Permissões', {'fields': ('is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Datas', {'fields': ('last_login','date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email','phone','password1','password2')}),
    )
    list_display = ('id','email','phone','full_name','is_active','is_staff')
    search_fields = ('email','phone','full_name')
    ordering = ('id',)