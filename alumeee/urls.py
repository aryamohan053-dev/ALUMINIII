# alumeee/urls.py

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from pages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('memory-gallery/', views.memory_gallery_view, name='memory_gallery'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
