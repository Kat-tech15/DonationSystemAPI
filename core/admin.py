from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count,Sum
from donations.models import Donation   
from beneficiaries.models import Beneficiary


class CustomAminView(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('impact-metrics/', self.admin_view(self.impact_mertrics_view), name='impact-metrics'),
        ]
        return custom_urls + urls
    
    def impact_mertrics_view(self, request):
        total_donations = Donation.objects.all()
        total_beneficiaries = Beneficiary.objects.filter(application_status='APPROVED').count()
        success_rate = (total_beneficiaries / Beneficiary.objects.count()) * 100 if Beneficiary.objects.count() > 0 else 0

        context = {
            'total_donations': total_donations,
            'total_beneficiaries': total_beneficiaries,
            'success_rate': success_rate
        }
        return render(request, 'admin/impact_metrics.html', context)
    

admin_site = CustomAminView(name='custom_admin')
admin_site.register(User, UserAdmin)
admin_site.register(Donation, DonationAdmin)
admin_site.register(Beneficiary, BeneficiaryAdmin, )
