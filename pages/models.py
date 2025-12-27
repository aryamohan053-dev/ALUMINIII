from django.db import models
from django.contrib.auth.models import User

# ================= Staff Profile =================
class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, null=True)
    qualification = models.CharField(max_length=200, blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    date_joined = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, default="Active")
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='staff_photos/', blank=True, null=True)
    office_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.designation}"


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


# ================= Memory (Gallery) =================


class Memory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='memories/', blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # optional if using admin approval

    def __str__(self):
        return self.title





# ================= Fund & Donation =================
class Fund(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_amount = models.IntegerField()
    collected_amount = models.IntegerField(default=0)
    image = models.ImageField(upload_to='funds/', blank=True, null=True)

    def __str__(self):
        return self.title


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} donated ₹{self.amount} to {self.fund}"


# ================= Notification =================
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.user.username}"


# ================= Departments & Students =================
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    year = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


# ================= Alumni =================
class Alumni(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    graduation_year = models.IntegerField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    current_company = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='alumni_photos/', blank=True, null=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class VerifiedAlumni(models.Model):
    alumni = models.OneToOneField(Alumni, on_delete=models.CASCADE, related_name='verification')
    is_verified = models.BooleanField(default=False)
    verified_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.alumni.user.username} - Verified: {self.is_verified}"


# ================= Event =================
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/', blank=True, null=True)

    def __str__(self):
        return self.title


# ================= Registered Students =================
class RegisteredStudent(models.Model):
    name = models.CharField(max_length=100)
    register_no = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    admission_year = models.IntegerField()

    def __str__(self):
        return self.name
