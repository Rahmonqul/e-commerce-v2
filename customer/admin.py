from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class AddressAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'full_name']

class WhishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_id', 'product']

class NotificationsAdmin(ImportExportModelAdmin):
    list_display = ['user', 'type', 'seen', 'date']

admin.site.register(Address, AddressAdmin)
admin.site.register(Whishlist, WhishlistAdmin)
# admin.site.register(Notifications, NotificationsAdmin)