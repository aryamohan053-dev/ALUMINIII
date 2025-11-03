from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import StudentProfile, StaffProfile


# ---------------- Home ----------------
def home_view(request):
    return render(request, 'home.html')


# ---------------- Register (Student / Faculty) ----------------
def register_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')

        # ---------- Student Registration ----------
        if role == 'student':
            name = request.POST.get('student_name')
            email = request.POST.get('student_email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            roll = request.POST.get('student_roll')
            dept = request.POST.get('student_dept')
            year = request.POST.get('student_year')
            phone = request.POST.get('student_phone')
            photo = request.FILES.get('student_photo')

            # Validation checks
            if password != confirm_password:
                messages.error(request, "❌ Passwords do not match!")
                return redirect('register')

            if User.objects.filter(email=email).exists():
                messages.error(request, "❌ Email already registered!")
                return redirect('register')

            # Create Django user and student profile
            user = User.objects.create_user(
                username=email,  # username same as email
                email=email,
                password=password,
                first_name=name
            )

            StudentProfile.objects.create(
                user=user,
                roll_number=roll,
                department=dept,
                passing_year=year,
                phone=phone,
                profile_photo=photo
            )

            messages.success(request, "✅ Student registered successfully!")
            return redirect('login')

        # ---------- Faculty Registration ----------
        elif role == 'teacher':
            faculty_id = request.POST.get('faculty_id')
            email = request.POST.get('teacher_email')
            password = request.POST.get('teacher_password')
            confirm_password = request.POST.get('teacher_confirm_password')
            designation = request.POST.get('designation')
            dept = request.POST.get('department')
            qualification = request.POST.get('qualification')
            experience = request.POST.get('experience')
            date_joined = request.POST.get('date_joined')
            status = request.POST.get('status')
            phone = request.POST.get('teacher_phone')
            photo = request.FILES.get('teacher_photo')

            # Validation checks
            if password != confirm_password:
                messages.error(request, "❌ Passwords do not match!")
                return redirect('register')

            if User.objects.filter(email=email).exists():
                messages.error(request, "❌ Email already registered!")
                return redirect('register')

            # Create Django user and staff profile
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=faculty_id
            )

            StaffProfile.objects.create(
                user=user,
                designation=designation,
                department=dept,
                qualification=qualification,
                experience=experience,
                date_joined=date_joined,
                status=status,
                phone=phone,
                profile_photo=photo
            )

            messages.success(request, "✅ Faculty registered successfully!")
            return redirect('login')

        # ---------- Invalid Role ----------
        else:
            messages.error(request, "❌ Please select a valid role!")
            return redirect('register')

    # ---------- GET Request (Render Page) ----------
    return render(request, 'register.html')



# ---------------- Login ----------------
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "✅ Login successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "❌ Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')


# ---------------- Logout ----------------
def logout_view(request):
    logout(request)
    messages.success(request, "✅ Logged out successfully!")
    return redirect('login')


# ---------------- Dashboard ----------------
def dashboard_view(request):
    return render(request, 'dashboard.html')


# ---------------- Profile ----------------
def profile_view(request):
    # Later: detect whether user is a student or staff and display accordingly
    return render(request, 'profile.html')


# ---------------- Memory Gallery ----------------
def memory_gallery_view(request):
    return render(request, 'memory_gallery.html')
