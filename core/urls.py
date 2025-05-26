from django.urls import path
from . import views as core_views

app_name = 'core'

urlpatterns = [
    path('', core_views.home_view, name='home'),

    path('samples/new/', core_views.sample_create_view, name='sample_create'),
    path('samples/success/', core_views.sample_success_view, name='sample_success'),

    # CRUD views
    path('samples/', core_views.SampleListView.as_view(), name='sample_list'),
    path('samples/<int:pk>/', core_views.SampleDetailView.as_view(), name='sample_detail'),
    path('samples/<int:pk>/edit/', core_views.SampleUpdateView.as_view(), name='sample_update'),
    path('samples/<int:pk>/delete/', core_views.SampleDeleteView.as_view(), name='sample_delete'),

    # Signup view
    path("accounts/signup/", core_views.signup_view, name="signup"),

    path('logout/', core_views.logout_confirm, name='logout_confirm'),
]
