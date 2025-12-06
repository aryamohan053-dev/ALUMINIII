from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # include pages app with namespace so {% url 'pages:...' %} works
    path('', include(('pages.urls', 'pages'), namespace='pages')),
]