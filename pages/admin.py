from django.contrib import admin
from .models import StudentProfile, StaffProfile, Memory

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'year_of_passing', 'department', 'phone')  # changed from 'batch_year'
    search_fields = ('user__username', 'user__email', 'roll_number')
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Name'

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'designation', 'office_number']
    search_fields = ['user__username', 'user__first_name']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Name'

@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_username', 'likes', 'created_at']
    search_fields = ['user__username', 'title']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'User'
