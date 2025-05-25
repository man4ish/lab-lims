from django.urls import path
from . import views

app_name = 'core'  # important!

urlpatterns = [
    path('samples/new/', views.sample_create_view, name='sample_create'),
    path('samples/success/', views.sample_success_view, name='sample_success'),
]
