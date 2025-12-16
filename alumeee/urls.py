# alumeee/urls.py

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from pages import views
from pages.views import students_list



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('student-home/', views.student_home_view, name='student_home'),
    path('staff-home/', views.staff_home_view, name='staff_home'),

    path('profile/', views.profile_view, name='profile'),
    path('memory-gallery/', views.memory_gallery_view, name='memory_gallery'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('memory/<int:pk>/', views.memory_detail_view, name='memory_detail'),
    path('memory-gallery/', views.memory_gallery_view, name='memory_gallery'),
    path('profile/<int:user_id>/', views.public_profile_view, name='public_profile'),

    path('fund-collection/', views.fund_collection, name='fund_collection'),
    path('fund/create/', views.create_fund, name='create_fund'),
     path("fund/donate/<int:fund_id>/", views.donate_fund, name="donate_fund"),


    path('notifications/', views.notifications, name='notifications'),
    path('staff/students/', views.students_list, name='students'),
]


# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
