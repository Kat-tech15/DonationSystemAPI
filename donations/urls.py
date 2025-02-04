from django.urls import path  
from .views import DonationCreateView, DonationListView, DonationDetailView


urlpatterns = [
    path('donations/', DonationCreateView.as_view(), name='donate'),
    path('donations/list/', DonationListView.as_view(), name='donation-list'),
    path('donations/<int:pk>/', DonationDetailView.as_view(),name='donation-detail'),
]