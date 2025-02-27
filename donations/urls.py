from django.urls import path  
from .views import DonationCreateView, DonationListView, DonationDetailView


urlpatterns = [
    path('api/donations/', DonationCreateView.as_view(), name='donate'),
    path('api/donations/list/', DonationListView.as_view(), name='donation-list'),
    path('api/donations/<int:pk>/', DonationDetailView.as_view(),name='donation-detail'),
]
