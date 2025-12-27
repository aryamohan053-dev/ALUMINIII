from django.contrib import admin
from .models import (
    StudentProfile, StaffProfile, Memory,
    Alumni, Event, Fund, Donation, Notification, Department, VerifiedAlumni
)

# ================= Admin Site Customization =================
admin.site.site_header = "Alumni Connect Admin"
admin.site.site_title = "Alumni Connect Admin Portal"
admin.site.index_title = "Welcome to Alumni Connect Admin Dashboard"

# ================= Helper Mixin for Full Name =================
class UserFullNameMixin:
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Name'

# ================= Student Profile Admin =================
@admin.register(StudentProfile)
class StudentProfileAdmin(UserFullNameMixin, admin.ModelAdmin):
    list_display = ('get_full_name', 'year_of_passing', 'department', 'phone')
    search_fields = ('user__username', 'user__email', 'roll_number')
    list_filter = ('department', 'year_of_passing')
    list_display_links = ('get_full_name',)
    readonly_fields = ('user',)
    ordering = ('year_of_passing', 'department')

# ================= Staff Profile Admin =================
@admin.register(StaffProfile)
class StaffProfileAdmin(UserFullNameMixin, admin.ModelAdmin):
    list_display = ('get_full_name', 'designation', 'office_number')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_filter = ('designation',)
    list_display_links = ('get_full_name',)
    readonly_fields = ('user',)
    ordering = ('designation',)

# ================= Memory Admin =================
@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_username', 'date_posted')
    search_fields = ('title', 'user__username', 'user__email')
    list_filter = ('date_posted',)
    readonly_fields = ('date_posted', 'user')
    list_display_links = ('title',)
    ordering = ('-date_posted',)
    date_hierarchy = 'date_posted'

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'User'

# ================= Alumni Admin =================
@admin.register(Alumni)
class AlumniAdmin(UserFullNameMixin, admin.ModelAdmin):
    list_display = ('get_full_name', 'graduation_year', 'department', 'current_company', 'role', 'is_blocked')
    search_fields = ('user__username', 'user__email', 'current_company', 'role')
    list_filter = ('department', 'graduation_year', 'is_blocked')
    list_display_links = ('get_full_name',)
    readonly_fields = ('user',)
    ordering = ('graduation_year', 'department')
    actions = ['block_alumni', 'unblock_alumni']

    @admin.action(description="Block selected alumni")
    def block_alumni(self, request, queryset):
        updated_count = queryset.update(is_blocked=True)
        self.message_user(request, f"{updated_count} alumni have been blocked.")

    @admin.action(description="Unblock selected alumni")
    def unblock_alumni(self, request, queryset):
        updated_count = queryset.update(is_blocked=False)
        self.message_user(request, f"{updated_count} alumni have been unblocked.")

# ================= Verified Alumni Admin =================
@admin.register(VerifiedAlumni)
class VerifiedAlumniAdmin(admin.ModelAdmin):
    list_display = (
        'get_name', 
        'get_email', 
        'get_register_no', 
        'get_department', 
        'get_passing_year', 
        'is_verified', 
        'verified_date'
    )
    list_filter = ('is_verified',)  # Only direct fields or fields on model
    search_fields = ('alumni__user__username', 'alumni__user__email', 'alumni__user__studentprofile__roll_number')

    def get_name(self, obj):
        return obj.alumni.user.get_full_name()
    get_name.short_description = 'Name'

    def get_email(self, obj):
        return obj.alumni.user.email
    get_email.short_description = 'Email'

    def get_register_no(self, obj):
        sp = getattr(obj.alumni.user, 'studentprofile', None)
        return sp.roll_number if sp else None
    get_register_no.short_description = 'Register No'

    def get_department(self, obj):
        return obj.alumni.department.name if obj.alumni.department else None
    get_department.short_description = 'Department'

    def get_passing_year(self, obj):
        sp = getattr(obj.alumni.user, 'studentprofile', None)
        return sp.year_of_passing if sp else None
    get_passing_year.short_description = 'Passing Year'

# ================= Notification Admin =================
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'is_read')
    search_fields = ('title', 'user__username')
    list_filter = ('is_read', 'created_at')
    readonly_fields = ('created_at', 'user')
    ordering = ('-created_at',)
    list_editable = ('is_read',)
    date_hierarchy = 'created_at'

# ================= Event Admin =================
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'location', 'created_by')
    search_fields = ('title', 'location', 'created_by__username')
    list_filter = ('start_date', 'end_date')
    list_display_links = ('title',)
    readonly_fields = ('created_by',)
    ordering = ('-start_date',)
    date_hierarchy = 'start_date'

# ================= Fund Admin =================
@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_amount', 'collected_amount')
    search_fields = ('title',)
    list_filter = ('title',)
    list_display_links = ('title',)
    ordering = ('title',)
    list_editable = ('collected_amount',)

# ================= Donation Admin =================
@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'fund', 'amount', 'donated_at')
    search_fields = ('user__username', 'fund__title')
    list_filter = ('fund', 'donated_at')
    readonly_fields = ('donated_at', 'user', 'fund')
    ordering = ('-donated_at',)
    date_hierarchy = 'donated_at'

# ================= Department Admin =================
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin, login_url='/login/')
def admin_dashboard(request):
    context = {
        'user': request.user,
        'students_count': StudentProfile.objects.count(),
        'alumni_count': Alumni.objects.count(),
        'events_count': Event.objects.count(),
        'pending_memories': Memory.objects.filter(is_approved=False).count(),
        'notifications_count': 3,
        'pending_approvals': 3,
    }
    return render(request, 'admin/admin_dashboard.html', context)
 
