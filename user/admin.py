from django.contrib import admin
from .models import CustomUser, Owner, Client

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'username', 'user_type')
    list_filter = ('user_type', 'date_joined', )
    search_fields = ('first_name', 'last_name', 'username')
    ordering = ('-date_joined',)

class OwnerAdmin(admin.ModelAdmin):
    list_display = ('owner', 'phone_number', 'properties')
    list_filter = ('owner', 'phone_number')
    search_fields = ('owner', 'phone_number')
    ordering = ('-owner',)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('customer', 'dob', 'phone_number', 'has_paid')
    list_filter = ('customer__username', 'phone_number' )
    ordering = ('-customer__username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Owner, OwnerAdmin)