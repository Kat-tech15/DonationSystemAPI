from django.urls import path 
from .views import BeneficiaryApplyView,BeneficiaryStatusView, BeneficiaryDetailview


urlpatterns =[
    path('apply/', BeneficiaryApplyView.as_view(), name='beneficiary-apply'),
    path('status/', BeneficiaryStatusView.as_view(), name='benefciary-status'),
    path('<int:pk>/', BeneficiaryDetailview.as_view(), name='beneficiary-detail'),
]