from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_id",
        "user",
        "payment_method",
        "amount",
        "currency",
        "status",
        "created_at",
    )
    search_fields = ("transaction_id", "user__username", "user__email")
    list_filter = ("payment_method", "status", "created_at")
    readonly_fields = ("transaction_id", "created_at", "updated_at")
    ordering = ("-created_at",)

    @admin.display(description='User')
    def user(self, obj):
        return obj.user.username

    @admin.action(description='Mark selected transactions as completed')
    def make_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, "Selected transactions have been marked as completed.")

    actions = [make_completed]
