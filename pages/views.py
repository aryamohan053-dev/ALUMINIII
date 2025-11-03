from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import StudentProfile, StaffProfile, Memory

# ---------------- Home ----------------
def home_view(request):
    return render(request, 'home.html')


# ---------------- Register ----------------
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

            if password != confirm_password:
                messages.error(request, "❌ Passwords do not match!")
                return redirect('register')

            if User.objects.filter(email=email).exists():
                messages.error(request, "❌ Email already registered!")
                return redirect('register')

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )

            StudentProfile.objects.create(
                user=user,
                roll_number=roll,
                department=dept,
                year_of_passing=year,
                phone=phone,
                photo=photo
            )

            messages.success(request, "✅ Student registered successfully!")
            return redirect('login')

        # ---------- Teacher Registration ----------
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

            if password != confirm_password:
                messages.error(request, "❌ Passwords do not match!")
                return redirect('register')

            if User.objects.filter(email=email).exists():
                messages.error(request, "❌ Email already registered!")
                return redirect('register')

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
                photo=photo
            )

            messages.success(request, "✅ Faculty registered successfully!")
            return redirect('login')

        else:
            messages.error(request, "❌ Please select a valid role!")
            return redirect('register')

    return render(request, 'register.html')


# ---------------- Login ----------------
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user:
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
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


# ---------------- Profile ----------------
@login_required
def profile_view(request):
    user = request.user
    profile = None
    role = None

    try:
        profile = user.studentprofile
        role = 'student'
    except StudentProfile.DoesNotExist:
        try:
            profile = user.staffprofile
            role = 'staff'
        except StaffProfile.DoesNotExist:
            role = 'unknown'

    context = {'profile': profile, 'role': role}
    return render(request, 'profile.html', context)


# ---------------- Memory Gallery ----------------
@login_required
def memory_gallery_view(request):
    memories = Memory.objects.all().order_by('-date_posted')
    return render(request, 'memory_gallery.html', {'memories': memories})
