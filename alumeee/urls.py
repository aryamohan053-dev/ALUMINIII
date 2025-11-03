# alumeee/urls.py

from django.contrib import admin
from django.urls import path
from pages import views  # importing views directly from your 'pages' app
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔹 Authentication routes
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),  # 👈 connects to your register view

    # 🔹 General app pages
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('memory-gallery/', views.memory_gallery_view, name='memory_gallery'),
]

# 🔹 Media configuration for image uploads (important for profile photos)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
