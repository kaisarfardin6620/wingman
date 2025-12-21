from django.contrib import admin
from .models import User, OneTimePassword

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'is_active', 'is_staff')
    search_fields = ('email', 'name')

admin.site.register(User, UserAdmin)
admin.site.register(OneTimePassword)