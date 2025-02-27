from django.urls import path
from .views import TestimonialListView, TestimonialCreateView
from .views import ImpactMerticsView


urlpatterns =[
    path('api/testimonials/', TestimonialListView.as_view(),name='testimonial-list'),
    path('api/testimonials/submit/', TestimonialCreateView.as_view(),name='testimonial-submit'),
    path('api/impact/metrics/', ImpactMerticsView.as_view(), name='impact-metrics'),
]