from django.urls import path 
from .views import BeneficiaryApplyView,BeneficiaryStatusView, BeneficiaryDetailview


urlpatterns =[
    path('api/beneficiaries/apply/', BeneficiaryApplyView.as_view(), name='beneficiary-apply'),
    path('api/beneficiaries/status/', BeneficiaryStatusView.as_view(), name='benefciary-status'),
    path('api/beneficiaries/<int:pk>/', BeneficiaryDetailview.as_view(), name='beneficiary-detail'),
]