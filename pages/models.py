from django.db import models
from django.contrib.auth.models import User

# ================= Staff Profile =================
class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    qualification = models.CharField(max_length=100, blank=True)
    experience = models.PositiveIntegerField(null=True, blank=True)
    date_joined = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Active','Active'), ('Inactive','Inactive')], default='Active')
    phone = models.CharField(max_length=15, blank=True)
    photo = models.ImageField(upload_to='staff_photos/', blank=True, null=True)

    def __str__(self):
        return self.user.username


# ================= Student Profile =================
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    year_of_passing = models.PositiveIntegerField()
    phone = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.roll_number}"


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
    alumni = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='memories/')
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.alumni.username}"
