from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import StudentProfile

# Import only models guaranteed to exist at module import time.
try:
    from .models import StudentProfile, Memory, StaffProfile
except Exception:
    StudentProfile = None
    Memory = None
    StaffProfile = None

try:
    from .models import Event, Donation
except Exception:
    Event = None
    Donation = None

# ---------------- Home ----------------
def home_view(request):
    return render(request, 'home.html')


# ---------------- Register ----------------
def register_view(request):
    if request.method == 'POST':
        role = request.POST.get('role', 'student')

        # Student form field names from template
        if role == 'student':
            full_name = request.POST.get('student_name', '').strip()
            email = request.POST.get('student_email', '').strip().lower()
            password = request.POST.get('password', '').strip()
            confirm = request.POST.get('confirm_password', '').strip()
            roll = request.POST.get('student_roll', '').strip()
            department = request.POST.get('student_dept', '').strip()
            year = request.POST.get('student_year', '').strip()
            phone = request.POST.get('student_phone', '').strip()
            photo = request.FILES.get('student_photo')

        # Teacher form field names
        else:
            full_name = request.POST.get('faculty_id', '').strip()
            email = request.POST.get('teacher_email', '').strip().lower()
            password = request.POST.get('teacher_password', '').strip()
            confirm = request.POST.get('teacher_confirm_password', '').strip()
            department = request.POST.get('department', '').strip()
            phone = request.POST.get('teacher_phone', '').strip()
            photo = request.FILES.get('teacher_photo')
            # teacher-specific extras (qualification, designation) can be read here

        # basic validation
        if not password:
            messages.error(request, 'Password is required.')
            return redirect('register')

        if password != confirm:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if not email and not full_name:
            messages.error(request, 'Provide an email or a name.')
            return redirect('register')

        if email and User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        # derive unique username
        base = email.split('@')[0] if email and '@' in email else ''.join(full_name.split()).lower() or 'user'
        username = base
        i = 1
        while User.objects.filter(username=username).exists():
            username = f"{base}{i}"
            i += 1

        # split name
        first_name = last_name = ''
        if full_name:
            parts = full_name.split()
            first_name = parts[0]
            last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''

        try:
            user = User.objects.create_user(
                username=username,
                email=email or '',
                password=password,
                first_name=first_name,
                last_name=last_name
            )
        except Exception as e:
            messages.error(request, f'Error creating user: {e}')
            return redirect('register')

        # create matching profile fields (use actual StudentProfile fields)
        try:
            if role == 'student' and StudentProfile:
                StudentProfile.objects.create(
                    user=user,
                    roll_number=roll,
                    year_of_passing=(int(year) if year.isdigit() else None),
                    phone=phone,
                    department=department or '',
                    profile_photo=photo
                )
            elif role != 'student' and StaffProfile:
                StaffProfile.objects.create(
                    user=user,
                    designation=request.POST.get('designation', ''),
                    phone=phone,
                    department=department or '',
                )
            else:
                # fallback when specific profile model is not available
                if StudentProfile:
                    StudentProfile.objects.get_or_create(user=user)
        except Exception:
            if StudentProfile:
                StudentProfile.objects.get_or_create(user=user)

        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')

    return render(request, 'register.html')


# ---------------- Login ----------------
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower().strip()
        password = request.POST.get('password')

        print("Email entered:", email)
        print("Password entered:", password)

        try:
            user = User.objects.get(email=email)
            print("User found:", user.username)
        except User.DoesNotExist:
            messages.error(request, "Email not registered.")
            print("ERROR: Email not found in database")
            return redirect('login')

        # Now authenticate using the stored username
        user_auth = authenticate(request, username=user.username, password=password)

        if user_auth:
            login(request, user_auth)
            messages.success(request, "🎉 Login successful!")
            print("SUCCESS: Logged in")
            return redirect('dashboard')
        else:
            messages.error(request, "Incorrect password.")
            print("ERROR: Wrong password - Authentication failed")
            return redirect('login')

    return render(request, 'login.html')


# ---------------- Forgot Password ----------------
def forgot_password_view(request):
    return render(request, 'forgot_password.html')


# ---------------- Logout ----------------
@login_required(login_url='login')
def logout_view(request):
    # log the user out and redirect to login (or another named URL)
    auth_logout(request)
    return redirect('login')


# ---------------- Dashboard ----------------
@login_required(login_url='login')
def dashboard_view(request):
    user = request.user

    # import optional models inside the view to avoid ImportError at module import time
    try:
        from .models import StudentProfile, Memory
    except Exception:
        StudentProfile = None
        Memory = None

    try:
        from .models import Event, Donation
    except Exception:
        Event = None
        Donation = None

    # student profile
    student_profile = None
    if StudentProfile:
        try:
            student_profile = StudentProfile.objects.filter(user=user).first()
        except Exception:
            student_profile = None

    # stats
    alumni_count = User.objects.count()
    memories_count = Memory.objects.filter(user=user).count() if Memory else 0
    recent_memories = Memory.objects.filter(user=user).order_by('-created_at')[:6] if Memory else []

    # events and donations (safe queries)
    upcoming_events = Event.objects.all().order_by('start_date')[:6] if Event else []
    donations = Donation.objects.all().order_by('-created_at')[:6] if Donation else []

    funds_total = 0
    if Donation:
        try:
            funds_total = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
        except Exception:
            funds_total = 0

    goal = 12540.0
    funds_percent = 0
    if goal:
        try:
            funds_percent = int(min(100, (float(funds_total) / goal) * 100))
        except Exception:
            funds_percent = 0

    context = {
        'user': user,
        'student_profile': student_profile,
        'alumni_count': alumni_count,
        'memories_count': memories_count,
        'recent_memories': recent_memories,
        'upcoming_events': upcoming_events,
        'donations': donations,
        'funds_total': funds_total,
        'funds_percent': funds_percent,
        'goal': int(goal),
    }
    return render(request, 'dashboard.html', context)


# ---------------- Profile ----------------
@login_required(login_url='login')
# ---------------- Profile View ----------------
@login_required(login_url='login')
def profile_view(request):
    user = request.user
    
    try:
        student_profile = StudentProfile.objects.get(user=user)
    except StudentProfile.DoesNotExist:
        student_profile = None
    
    return render(request, 'profile.html', {
        'user': user,
        'student_profile': student_profile
    })


# ---------------- Profile Edit View ----------------
@login_required(login_url='login')
def profile_edit_view(request):
    student_profile, created = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # --- User fields ---
        user = request.user
        full_name = request.POST.get("full_name", "").strip()

        if full_name:
            parts = full_name.split()
            user.first_name = parts[0]
            user.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        
        user.email = request.POST.get("email", "")
        user.save()

        # --- Student Profile fields ---
        student_profile.department = request.POST.get("department")
        student_profile.phone = request.POST.get("phone")
        student_profile.location = request.POST.get("location")
        student_profile.current_company = request.POST.get("current_company")
        student_profile.role = request.POST.get("role")

        # ============ FIX FOR BATCH & YEAR OF PASSING ============
        batch = request.POST.get("batch")

        # Save batch as text
        student_profile.batch = batch if batch else None

        # Save year_of_passing only if batch is numeric
        if batch and batch.isdigit():
            student_profile.year_of_passing = int(batch)
        else:
            student_profile.year_of_passing = None
        # ==========================================================

        # --- fix experience years ---
        exp_years = request.POST.get("experience_years")
        if exp_years and exp_years.isdigit():
            student_profile.experience_years = int(exp_years)
        else:
            student_profile.experience_years = None

        # profile photo
        if "profile_photo" in request.FILES:
            student_profile.profile_photo = request.FILES["profile_photo"]

        student_profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("pages:profile")

    return render(request, "profile_edit.html", {"student_profile": student_profile})


# ---------------- Memory Gallery ----------------
@login_required(login_url='login')
def memory_gallery_view(request):
    user = request.user
    memories = Memory.objects.filter(user=user).order_by('-created_at')
    
    return render(request, 'memory_gallery.html', {
        'user': user,
        'memories': memories
    }) 