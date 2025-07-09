from django.contrib import admin
from .models import Donation

@admin.action(description='Mark selected donations as approved')
def approve_donations(modeladmin, request, queryset):
    queryset.update(status='APPROVED')

@admin.action(description='Mark selected donations as rejected')
def reject_donations(modeladmin, request, queryset):
    queryset.update(status='REJECTED')

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'donation_type', 'amount', 'status', 'timestamp')
    list_filter = ('donation_type', 'status')  
    search_fields = ('donor__username', 'tracking_code') 
    actions = [approve_donations, reject_donations]
