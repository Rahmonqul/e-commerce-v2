from django.contrib import admin
from .models import *
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ['store_name', "user", 'country', 'vendor_id', 'date']
    search_fields = ['store_name', 'user__username', 'vendor_id']
    prepopulated_fields = {'slug': ('store_name',)}
    list_filter = ['country', 'date']

class PayoutAdmin(admin.ModelAdmin):
    list_display = ['payout_id', "vendor", 'item', 'amount', 'date']
    search_fields = ['payout_id', 'vendor__store_name', 'item__order__order_id']
    list_filter = ['vendor', 'date']

class BankAccontAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'bank_name', 'account_number', 'account_type']
    search_fields = ['vendor__store_name', 'bank_name', 'account_number']
    list_filter = ['account_type']

class NotificationsAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'order', 'seen']
    list_editable = ['order']

class StoreReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'store', 'rating', 'active', 'date']
    search_fields = ['user__username', 'vendor__store_name']
    list_filter = ['active', 'rating']

admin.site.register(Vendor, VendorAdmin)
admin.site.register(Payout, PayoutAdmin)
admin.site.register(BankAccount, BankAccontAdmin)
# admin.site.register(Notifications, NotificationsAdmin)
admin.site.register(StoreReview, StoreReviewAdmin)