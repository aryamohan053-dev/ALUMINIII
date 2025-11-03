# pages/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Home
    path('', views.home_view, name='home'),

    # 👤 Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),

    # 📊 Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # 🧍 Profile
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),

    # 🖼️ Memory Gallery
    path('memory-gallery/', views.memory_gallery_view, name='memory_gallery'),
]
