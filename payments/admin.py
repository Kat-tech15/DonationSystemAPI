from django.contrib import admin
from .models import Transaction

# Register your models here.

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("payment_method", "transaction_id", "amount", "status", "created_at")
    search_fields = ("transaction_id",)
    list_filter = ("payment_method", "status")