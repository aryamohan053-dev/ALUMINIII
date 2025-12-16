from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import StaffProfile, StudentProfile, Memory
from .forms import MemoryForm
from .models import Fund
from .models import Notification
from django.http import HttpResponseForbidden
from .models import Student, Department, StaffProfile

from django.utils import timezone




# ---------------- Home ----------------
@login_required(login_url='login')
def home_view(request):
    """Redirect users to the appropriate home page based on role."""
    user = request.user

    if StaffProfile.objects.filter(user=user).exists():
        return redirect('pages:staff_home')
    elif StudentProfile.objects.filter(user=user).exists():
        return redirect('pages:student_home')
    else:
        return render(request, "home.html")

# ---------------- Student Home ----------------
@login_required(login_url='login')
def student_home_view(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    recent_memories = Memory.objects.filter(user=request.user).order_by('-date_posted')[:6]


    return render(request, "student_home.html", {
        "student": student,
        "recent_memories": recent_memories,
    })

# ---------------- Staff Home ----------------
@login_required(login_url='login')
def staff_home_view(request):
    staff = StaffProfile.objects.filter(user=request.user).first()

    if not staff:
        messages.error(request, "You are not authorized as staff.")
        return redirect('pages:home')

    return render(request, "staff_home.html", {
        "staff": staff
    })

@login_required(login_url='login')
def dashboard_view(request):
    # your existing dashboard code here
    return render(request, "dashboard.html")
def forgot_password_view(request):
    return render(request, "forgot_password.html")

# ---------------- Register ----------------
def register_view(request):
    if request.method == "POST":
        role = request.POST.get("role")

        # -------------------------
        # STUDENT REGISTRATION
        # -------------------------
        if role == "student":
            name = request.POST.get("student_name", "").strip()
            email = request.POST.get("student_email", "").strip()
            password = request.POST.get("password", "")
            roll = request.POST.get("student_roll", "").strip()
            dept = request.POST.get("student_dept", "").strip()
            year = request.POST.get("student_year", "").strip()
            phone = request.POST.get("student_phone", "").strip()
            photo = request.FILES.get("student_photo")

            # Check duplicate email
            if User.objects.filter(username=email).exists():
                messages.error(request, "Email is already registered")
                return redirect("register")

            # Create Django User
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )

            # Create StudentProfile
            

            messages.success(request, "Student account created successfully!")
            return redirect("login")

        # -------------------------
        # TEACHER / STAFF REGISTRATION
        # -------------------------
        elif role == "teacher":
            name = request.POST.get("faculty_id", "").strip()
            email = request.POST.get("teacher_email", "").strip()
            password = request.POST.get("teacher_password", "")
            designation = request.POST.get("designation", "").strip()
            department = request.POST.get("department", "").strip()
            qualification = request.POST.get("qualification", "").strip()
            experience = request.POST.get("experience", "").strip()
            date_joined = request.POST.get("date_joined", "").strip()
            status = request.POST.get("status", "").strip()
            phone = request.POST.get("teacher_phone", "").strip()
            profile_photo = request.FILES.get("teacher_photo")

            # Check duplicate email
            if User.objects.filter(username=email).exists():
                messages.error(request, "Email is already registered")
                return redirect("pages:register")

            # Create Django User
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )

            # Create StaffProfile
            StaffProfile.objects.create(
                user=user,
                designation=designation,
                department=department,
                qualification=qualification,
                experience=experience,
                date_joined=date_joined,
                status=status,
                phone=phone,
                profile_photo=profile_photo
            )

            messages.success(request, "Teacher/Staff account created successfully!")
            return redirect("login")

        # -------------------------
        # INVALID ROLE
        # -------------------------
        else:
            messages.error(request, "Invalid role selected")
            return redirect("pages:register")

    # -------------------------
    # GET REQUEST
    # -------------------------
    return render(request, "register.html")


# ---------------- Login ----------------
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Find user by email
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email does not exist")
            return redirect("pages:login")

        user = authenticate(request, username=user_obj.username, password=password)

        if user is None:
            messages.error(request, "Wrong password")
            return redirect("pages:login")

        login(request, user)

        # ROLE CHECK
        if StaffProfile.objects.filter(user=user).exists():
            return redirect("pages:staff_home")

        if StudentProfile.objects.filter(user=user).exists():
            return redirect("pages:student_home")

        return redirect("pages:home")

    return render(request, "login.html")


# ---------------- Logout ----------------
@login_required(login_url='login')
def logout_view(request):
    auth_logout(request)
    return redirect('login')


# ---------------- Profile ----------------
@login_required(login_url='login')
def profile_view(request):
    user = request.user
    student_profile = StudentProfile.objects.filter(user=user).first()
    staff_profile = StaffProfile.objects.filter(user=user).first()

    return render(request, 'profile.html', {
        'user': user,
        'student_profile': student_profile,
        'staff_profile': staff_profile
    })


# ---------------- Profile Edit ----------------
@login_required(login_url='login')
def profile_edit_view(request):
    user = request.user
    student_profile = StudentProfile.objects.filter(user=user).first()
    staff_profile = StaffProfile.objects.filter(user=user).first()

    if request.method == "POST":
        # --- User fields ---
        full_name = request.POST.get("full_name", "").strip()
        if full_name:
            parts = full_name.split()
            user.first_name = parts[0]
            user.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        user.email = request.POST.get("email", "")
        user.save()

        # --- Student profile ---
        if student_profile:
            student_profile.department = request.POST.get("department")
            student_profile.phone = request.POST.get("phone")
            student_profile.location = request.POST.get("location")
            student_profile.current_company = request.POST.get("current_company")
            student_profile.role = request.POST.get("role")
            batch = request.POST.get("batch")
            student_profile.batch = batch if batch else None
            student_profile.year_of_passing = int(batch) if batch and batch.isdigit() else None
            exp_years = request.POST.get("experience_years")
            student_profile.experience_years = int(exp_years) if exp_years and exp_years.isdigit() else None
            if "profile_photo" in request.FILES:
                student_profile.profile_photo = request.FILES["profile_photo"]
            student_profile.save()

        # --- Staff profile ---
        if staff_profile:
            staff_profile.phone = request.POST.get("phone")
            staff_profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("pages:profile")

    return render(request, "profile_edit.html", {
        "student_profile": student_profile,
        "staff_profile": staff_profile
    })


# ---------------- Memory Gallery ----------------
@login_required(login_url='login')
def memory_gallery_view(request):
    if request.method == 'POST':
        form = MemoryForm(request.POST, request.FILES)
        if form.is_valid():
            memory = form.save(commit=False)
            memory.user = request.user
            memory.save()
            return redirect('memory_gallery')
    else:
        form = MemoryForm()

    memories = Memory.objects.all().order_by('-date_posted')
    return render(request, 'memory_gallery.html', {
        'form': form,
        'memories': memories
    })


@login_required(login_url='login')
def memory_detail_view(request, pk):
    memory = get_object_or_404(Memory, pk=pk)

    # 🔒 Allow only owner to view full memory
    if memory.user != request.user:
        return HttpResponseForbidden("You are not allowed to view this memory.")

    return render(request, 'memory_detail.html', {'memory': memory})

@login_required(login_url='login')
def fund_collection(request):
    funds = Fund.objects.all()
    return render(request, 'pages/fund_collection.html', {'funds': funds})

@login_required(login_url='login')
def public_profile_view(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)

    student_profile = StudentProfile.objects.filter(user=profile_user).first()
    staff_profile = StaffProfile.objects.filter(user=profile_user).first()

    return render(request, 'public_profile.html', {
        'profile_user': profile_user,
        'student_profile': student_profile,
        'staff_profile': staff_profile
    })

@login_required(login_url='login')
def create_fund(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        target_amount = request.POST.get("target_amount")
        image = request.FILES.get("image")

        # 🔒 SAFETY CHECK
        if not title or not target_amount:
            messages.error(request, "Title and target amount are required")
            return redirect("create_fund")

        Fund.objects.create(
            title=title,
            description=description,
            target_amount=target_amount,
            image=image
        )

        messages.success(request, "Fund created successfully")
        return redirect("fund_collection")

    return render(request, "create_fund.html")


@login_required(login_url='login')
def donate_fund(request, fund_id):
    fund = get_object_or_404(Fund, id=fund_id)

    if request.method == "POST":
        amount = int(request.POST.get("amount"))

        # Update collected amount
        fund.collected_amount += amount
        fund.save()

        messages.success(request, "Thank you for your donation!")
        return redirect("fund_collection")

    return render(request, "donate_fund.html", {"fund": fund})





def notifications(request):
    return render(request, 'pages/notifications.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pages.models import StudentProfile, Department
from django.db.models import Count, Q
import datetime

@login_required
def students_list(request):
    # Get all students - check what field you have for ordering
    # Common fields might be: id, user__date_joined, or check if you have a registration date field
    students = StudentProfile.objects.all().order_by('-id')  # Order by ID (newest first)
    
    # Check what fields your StudentProfile model actually has
    # Based on error, available fields are: batch, current_company, department, experience_years, 
    # id, location, phone, profile_photo, role, roll_number, user, user_id, year_of_passing
    
    # If you want to order by user creation date (if it exists)
    # students = StudentProfile.objects.all().order_by('-user__date_joined')
    
    # Calculate stats
    current_year = datetime.datetime.now().year
    
    context = {
        'students': students,
        'active_students': students.count(),  # Or filter by some active status if you have it
        'graduating_this_year': students.filter(
            Q(year_of_passing=str(current_year)) | Q(year_of_passing=current_year)
        ).count(),
        'departments_count': Department.objects.count(),
        'departments': Department.objects.all(),
    }
    return render(request, "pages/students_list.html", context)

@login_required(login_url='login')
def dashboard_view(request):
    return render(request, "dashboard.html")


