# pages/urls.py
from django.urls import path
from . import views
from pages.views import students_list

app_name = 'pages'

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
    path('student-home/', views.student_home_view, name='student_home'),
    path('staff-home/', views.staff_home_view, name='staff_home'),

    # 🧍 PUBLIC PROFILE (⚠️ MUST COME FIRST)
    path('profile/<int:user_id>/', views.public_profile_view, name='public_profile'),

    # 🧍 PRIVATE PROFILE
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),

    # 🖼️ Memory Gallery
    path('memory-gallery/', views.memory_gallery_view, name='memory_gallery'),
    path('memory/<int:pk>/', views.memory_detail_view, name='memory_detail'),

    # 💰 Funds
    path('fund-collection/', views.fund_collection, name='fund_collection'),
    path('fund/create/', views.create_fund, name='create_fund'),

    # 🔔 Notifications
    path('notifications/', views.notifications, name='notifications'),

     path('staff/students/', students_list, name='students_list'),
]
