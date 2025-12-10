from django.db import models
from django.contrib.auth.models import User

# ================= Staff Profile =================
class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    office_number = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.designation}"


# ================= Student Profile =================
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=50, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    batch = models.CharField(max_length=20, blank=True, null=True)
    year_of_passing = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    current_company = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    experience_years = models.IntegerField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    
    # ADD THIS
    location = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

    
    @property
    def batch_year(self):
        return self.year_of_passing


# ================= Admin Profile =================
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username


# ================= User Profile =================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


# ================= Memory (for Gallery) =================
class Memory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='memories/')
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    class Meta:
        ordering = ['-created_at']
