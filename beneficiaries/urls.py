from django.urls import path 
from .views import BeneficiaryApplyView,BeneficiaryStatusView, BeneficiaryDetailview


urlpatterns =[
    path('beneficiaries/apply/', BeneficiaryApplyView.as_view(), name='beneficiary-apply'),
    path('beneficiaries/status/', BeneficiaryStatusView.as_view(), name='benefciary-status'),
    path('beneficiaries/<int:pk>/', BeneficiaryDetailview.as_view(), name='beneficiary-detail'),
]