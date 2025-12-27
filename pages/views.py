from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.db.models import Q
import datetime
from pages.models import StudentProfile
from django.contrib.auth.models import User


from .models import StudentProfile, Memory, Fund, Student, Department, Alumni,Event
from .forms import MemoryForm


# ---------------- Helper Functions ----------------
def is_admin(user):
    return user.is_authenticated and user.is_superuser


# ---------------- Home ----------------
@login_required(login_url='login')
def home_view(request):
    """Redirect users to the appropriate home page based on role."""
    user = request.user

    if user.is_superuser:
        return redirect('pages:admin_dashboard')
    elif StudentProfile.objects.filter(user=user).exists():
        return redirect('pages:student_home')
    else:
        return render(request, "home.html")
def is_admin(user):
    return user.is_authenticated and user.is_superuser


# ---------------- Dashboard (Admin Only) ----------------
@user_passes_test(is_admin, login_url='login')
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
    return render(request, 'pages/admin_dashboard.html', context)

@login_required(login_url='login')
def dashboard_redirect(request):
    if request.user.is_superuser:
        return redirect('pages:admin_dashboard')
    elif StudentProfile.objects.filter(user=request.user).exists():
        return redirect('pages:student_home')
    else:
        return redirect('pages:home')






# ---------------- Student Home ----------------
@login_required(login_url='login')
def student_home_view(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    recent_memories = Memory.objects.filter(user=request.user).order_by('-date_posted')[:6]

    return render(request, "student_home.html", {
        "student": student,
        "recent_memories": recent_memories,
    })


# ---------------- Forgot Password ----------------
def forgot_password_view(request):
    return render(request, "forgot_password.html")


# ---------------- Register ----------------
def register_view(request):
    if request.method == "POST":
        role = request.POST.get("role")

        if role == "student":
            name = request.POST.get("student_name", "").strip()
            email = request.POST.get("student_email", "").strip()
            password = request.POST.get("password", "")
            roll = request.POST.get("student_roll", "").strip()
            dept = request.POST.get("student_dept", "").strip()
            year = request.POST.get("student_year", "").strip()
            phone = request.POST.get("student_phone", "").strip()
            photo = request.FILES.get("student_photo")

            if User.objects.filter(username=email).exists():
                messages.error(request, "Email is already registered")
                return redirect("register")

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
                profile_photo=photo
            )

            messages.success(request, "Student account created successfully!")
            return redirect("login")

        else:
            messages.error(request, "Invalid role selected")
            return redirect("pages:register")

    return render(request, "register.html")


# ---------------- Login ----------------
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

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

        if user.is_superuser:
            return redirect('pages:admin_dashboard')
        elif StudentProfile.objects.filter(user=user).exists():
            return redirect("pages:student_home")
        else:
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

    return render(request, 'profile.html', {
        'user': user,
        'student_profile': student_profile,
    })


@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')



# ---------------- Profile Edit ----------------
@login_required(login_url='login')
def profile_edit_view(request):
    user = request.user
    student_profile = StudentProfile.objects.filter(user=user).first()

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        if full_name:
            parts = full_name.split()
            user.first_name = parts[0]
            user.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        user.email = request.POST.get("email", "")
        user.save()

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

        messages.success(request, "Profile updated successfully.")
        return redirect("pages:profile")

    return render(request, "profile_edit.html", {
        "student_profile": student_profile
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


@login_required
def memory_detail_view(request, pk):
    memory = get_object_or_404(Memory, pk=pk)
    return render(request, 'pages/memory_detail.html', {'memory': memory})



# ---------------- Fund Collection ----------------
@login_required(login_url='login')
def fund_collection(request):
    funds = Fund.objects.all()
    return render(request, 'pages/fund_collection.html', {'funds': funds})


@login_required(login_url='login')
def create_fund(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        target_amount = request.POST.get("target_amount")
        image = request.FILES.get("image")

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
        fund.collected_amount += amount
        fund.save()
        messages.success(request, "Thank you for your donation!")
        return redirect("fund_collection")

    return render(request, "donate_fund.html", {"fund": fund})


# ---------------- Notifications ----------------
def notifications(request):
    return render(request, 'pages/notifications.html')


# ---------------- Students List ----------------
@login_required
def students_list(request):
    students = StudentProfile.objects.all().order_by('-id')
    current_year = datetime.datetime.now().year

    context = {
        'students': students,
        'active_students': students.count(),
        'graduating_this_year': students.filter(
            Q(year_of_passing=str(current_year)) | Q(year_of_passing=current_year)
        ).count(),
        'departments_count': Department.objects.count(),
        'departments': Department.objects.all(),
    }
    return render(request, "pages/students_list.html", context)


# ---------------- Alumni Verification (Admin Only) ----------------
@user_passes_test(is_admin, login_url='login')
def alumni_verification(request):
    students = Student.objects.all()
    verified_alumni = Alumni.objects.filter(is_verified=True)
    fake_alumni = Alumni.objects.filter(is_verified=False)

    context = {
        'students': students,
        'verified_alumni': verified_alumni,
        'fake_alumni': fake_alumni,
    }

    return render(request, 'admin/alumni_verification.html', context)


@user_passes_test(is_admin, login_url='login')
def verify_alumni(request, id):
    alumni = get_object_or_404(Alumni, id=id)
    is_real = Student.objects.filter(
        register_no=alumni.register_no,
        department=alumni.department,
    ).exists()

    if is_real:
        alumni.is_verified = True
        alumni.verified_date = timezone.now()
        alumni.save()

    return redirect('pages:alumni_verification')


@user_passes_test(is_admin, login_url='login')
def reject_alumni(request, id):
    alumni = get_object_or_404(Alumni, id=id)
    alumni.delete()
    return redirect('pages:alumni_verification')

@login_required
def public_profile_view(request, user_id):
    # Get the clicked user
    profile_user = get_object_or_404(User, id=user_id)

    # Get that user's student profile
    student_profile = get_object_or_404(StudentProfile, user=profile_user)

    return render(request, 'pages/public_profile.html', {
        'profile_user': profile_user,
        'student_profile': student_profile,
    })

# views.py (add this to your view)
@login_required
def delete_student(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, id=student_id)
        student_name = student.user.get_full_name() or student.user.username
        student.delete()
        messages.success(request, f'Student "{student_name}" has been deleted successfully.')
        return redirect('students_list')  # Change this to your actual list view name
    else:
        # If not POST, redirect to list
        return redirect('students_list')
    
    