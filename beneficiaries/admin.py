from django.contrib import admin
from .models import Beneficiary

# Register your models here.
admin.site.register(Beneficiary)

#@admin.action(description='approve selected beneficiaries')
def approve_beneficiaries(modeladmin, request, queryset):
    queryset.update(application_status='APPROVED')

#@admin.action(description='reject selected beneficiaries')
def reject_beneficiaries(modeladmin, request, queryset):
    queryset.update(application_status='REJECTED')

#@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'needy_status', 'education_level','application_status')
    list_filter = ('needy_status','application_status')
    search_fields = ('user__username', 'institution_name')
    actions = [approve_beneficiaries, reject_beneficiaries]