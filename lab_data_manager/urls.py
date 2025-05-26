"""
URL configuration for lab_data_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth URLs
    path("accounts/login/", auth_views.LoginView.as_view(template_name='registration/login.html'), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Core app URLs
    path('core/', include('core.urls', namespace='core')),

    # Redirect root URL to core home
    path('', RedirectView.as_view(url='/core/', permanent=False)),
]
