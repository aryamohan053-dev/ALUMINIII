from django.contrib import admin
from .models import StaffProfile, AdminProfile, UserProfile

admin.site.register(StaffProfile)
admin.site.register(AdminProfile)
admin.site.register(UserProfile)
