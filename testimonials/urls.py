from django.urls import path
from .views import TestimonialListView, TestimonialCreateView
from .views import ImpactMerticsView


urlpatterns =[
    path('testimonials/', TestimonialListView.as_view(),name='testimonial-list'),
    path('testimonials/submit/', TestimonialCreateView.as_view(),name='testimonial-submit'),
    path('impact/metrics/', ImpactMerticsView.as_view(), name='impact-metrics'),
]