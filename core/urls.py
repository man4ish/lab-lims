from django.urls import path
from . import views as core_views
from . import views
from .views import LibraryDetailView, LibraryUpdateView, LibraryDeleteView, LibraryLaneDetailView
app_name = 'core'

urlpatterns = [
    path('', core_views.home_view, name='home'),

    path('samples/new/', core_views.sample_create_view, name='sample_create'),
    path('samples/success/', core_views.sample_success_view, name='sample_success'),

    path('samples/', core_views.SampleListView.as_view(), name='sample_list'),
    # Change here to use the new view function
    path('samples/<int:pk>/', core_views.SampleDetailView.as_view(), name='sample_detail'),
    path('samples/<int:pk>/edit/', core_views.SampleUpdateView.as_view(), name='sample_update'),
    path('samples/<int:pk>/delete/', core_views.SampleDeleteView.as_view(), name='sample_delete'),

    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('library/<int:pk>/update/', LibraryUpdateView.as_view(), name='library_update'),
    path('library/<int:pk>/delete/', LibraryDeleteView.as_view(), name='library_delete'),

    path('librarylane/<int:pk>/', LibraryLaneDetailView.as_view(), name='librarylane_detail'),
    path('lane/<int:pk>/', views.LaneDetailView.as_view(), name='lane_detail'),

    path('analyses/flowcell/<int:flowcell_id>/', views.analyses_by_flowcell, name='analyses_by_flowcell'),


    path("accounts/signup/", core_views.signup_view, name="signup"),
    path('logout/', views.logout_confirm, name='logout_confirm'),
]
  