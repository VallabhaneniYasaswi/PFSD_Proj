from django.shortcuts import render, HttpResponse, redirect
from .models import Register
from .models import Student, Attendance
from django.contrib import messages
from datetime import date
# Create your views
def demo(request):
    return HttpResponse("<h1>Welcome to KLU</h1>")
def index(request):
    return render(request,'index.html')
def home(request):
    return render(request,'home.html')
def login(request):
    return render(request,'login.html')
def contact(request):
    return render(request,'contact.html')
def about(request):
    return render(request,'about.html')
def info(request):
    return render(request,'info.html')

def signup(request):
    return render(request,'signup.html')
def dashboard(request):
    return render(request,'dashboard.html')
def attendance(request):
    return render(request,'attendance.html')
def employee(request):
    return render(request,'employee.html')

def logout(request):
    request.session.flush()
    return redirect('login')
def teacher_management(request):
    # You can render a page for teacher management here
    return render(request, "teacher_management.html")


# def authendication(request):
#     if request.method == "POST":
#         adminuname = request.POST["uname"]  # gets user name
#         adminpwd = request.POST["pwd"]
#         flag = Register.objects.filter(username=adminuname, password=adminpwd).values()
#         if flag:
#             #return render(request, "TravelManagementhome.html")
#             return HttpResponse("<h1>Login Success</h1>")
#         else:
#             return HttpResponse("<h1>Login Failed</h1>")

def authendication(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        pwd = request.POST.get("pwd")

        try:
            user = Register.objects.get(username=uname, password=pwd)

            # ✅ Store session
            request.session['username'] = user.username
            request.session['role'] = user.role
            request.session.modified = True

            print("✅ LOGIN SUCCESS")
            print("Saved session:", dict(request.session))

            # Redirect based on role
            if user.role == "admin":
                return redirect('dashboard')
            elif user.role == "teacher":
                return redirect('attendance')
            elif user.role == "student":
                request.session["username"] = user.username
                request.session["role"] = "student"
                print(f"✅ STUDENT LOGIN SUCCESS: {user.username}")
                return redirect("student_home")
            else:
                return HttpResponse("<h3>Role not defined in database</h3>")

        except Register.DoesNotExist:
            print("❌ Invalid credentials")
            return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")




# def authendication(request):
#     if request.method == "POST":
#         uname = request.POST["uname"]
#         pwd = request.POST["pwd"]
#
#         try:
#             user = Register.objects.get(username=uname, password=pwd)
#
#             # Role-based redirection
#             if user.role == "admin":
#                 return render(request, "dashboard.html")
#             elif user.role == "teacher":
#                 return render(request, "attendance.html")
#             elif user.role == "student":
#                 return render(request, "employee.html")
#             else:
#                 return HttpResponse("<h1>Role not defined</h1>")
#
#         except Register.DoesNotExist:
#             return HttpResponse("<h1>Login Failed</h1>")


# def checkregistration(request):
#     if request.method == "POST":
#         name = request.POST["name"]
#         addr = request.POST["addr"]
#         email = request.POST["email"]
#         phno = request.POST["phno"]
#         uname = request.POST["uname"]
#         pwd = request.POST["pwd"]
#         cpwd = request.POST["cpwd"]
#         role = request.POST["role"]
#
#         if pwd != cpwd:
#             return render(request, "signup.html", {"error": "Passwords do not match"})
#
#         if Register.objects.filter(username=uname).exists():
#             return render(request, "signup.html", {"error": "Username already exists"})
#
#         if Register.objects.filter(email=email).exists():
#             return render(request, "signup.html", {"error": "Email already exists"})
#
#         # Create new user
#         user = Register.objects.create(
#             name=name,
#             address=addr,
#             email=email,
#             phno=phno,
#             username=uname,
#             password=pwd,
#             role=role
#         )
#         user.save()
#         return render(request, "login.html", {"success": "User registered successfully"})
#
#     return render(request, "signup.html")


def checkregistration(request):
    if request.method == "POST":
        name = request.POST["name"]
        addr = request.POST["addr"]
        email = request.POST["email"]
        phno = request.POST["phno"]
        uname = request.POST["uname"]
        pwd = request.POST["pwd"]
        cpwd = request.POST["cpwd"]
        role = request.POST["role"]

        if pwd != cpwd:
            return render(request, "signup.html", {"error": "Passwords do not match"})

        if Register.objects.filter(username=uname).exists():
            return render(request, "signup.html", {"error": "Username already exists"})

        if Register.objects.filter(email=email).exists():
            return render(request, "signup.html", {"error": "Email already exists"})

        # ✅ Create new user in Register table
        # Create new user in Register table
        user = Register.objects.create(
            name=name,
            address=addr,
            email=email,
            phno=phno,
            username=uname,
            password=pwd,
            role=role
        )
        user.save()  # Make sure to save before generating the roll_no

        # Automatically add to student_table if role = 'student'
        if role.lower() == "student":
            from .models import Student
            Student.objects.create(
                name=name,
                roll_no=f"STU{user.id:03d}",  # Generate roll number only after user has been saved
                department="CSE",  # you can later add a form field for this
                year=1,  # default 1st year
                email=email
            )

        return render(request, "login.html", {"success": "User registered successfully"})

    return render(request, "signup.html")

from datetime import date
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student, Attendance

def attendance(request):
    print("📂 SESSION DATA:", dict(request.session))  # debug line

    username = request.session.get('username')
    role = request.session.get('role')

    if not username or role != 'teacher':
        print("❌ Unauthorized access. username:", username, "role:", role)
        return HttpResponse("<h3>Unauthorized access. Please login as teacher.</h3>")

    teacher_username = username

    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("student_"):
                student_id = key.split("_")[1]
                status = value
                student = Student.objects.get(id=student_id)
                Attendance.objects.create(
                    student=student,
                    status=status,
                    marked_by=teacher_username
                )
        messages.success(request, "Attendance marked successfully!")
        return redirect('attendance')

    students = Student.objects.all()
    return render(request, "attendance.html", {"students": students, "today": date.today()})


from django.shortcuts import render, redirect
from .models import Student, Register

def student_home(request):
    # ✅ Ensure the student is logged in
    if request.session.get("role") != "student":
        return render(request, "unauthorized.html", {"message": "Please login as student."})

    username = request.session.get("username")
    user = Register.objects.get(username=username)

    # Check if student details already exist
    student = Student.objects.filter(email=user.email).first()

    if student:
        return redirect('student_profile')  # redirect to profile if already filled
    else:
        return render(request, "student_details.html")


def save_student_details(request):
    if request.method == "POST":
        username = request.session.get("username")
        user = Register.objects.get(username=username)

        name = user.name
        roll_no = f"STU{user.id:03d}"
        department = request.POST["department"]
        year = request.POST["year"]
        email = user.email

        # ✅ Save new student record
        Student.objects.create(
            name=name,
            roll_no=roll_no,
            department=department,
            year=year,
            email=email
        )
        return redirect('student_profile')
    else:
        return redirect('student_home')


def student_profile(request):
    if request.session.get("role") != "student":
        return render(request, "unauthorized.html", {"message": "Please login as student."})

    username = request.session.get("username")
    user = Register.objects.get(username=username)
    student = Student.objects.filter(email=user.email).first()

    if request.method == "POST" and student:
        roll_no = request.POST.get("roll_no")
        name = request.POST.get("name")
        department = request.POST.get("department")
        year = request.POST.get("year")
        email = request.POST.get("email")

        # 🟢 Ensure roll number uniqueness
        if roll_no != student.roll_no:  # Only check if the roll_no is changed
            existing_roll_no = Student.objects.filter(roll_no=roll_no).exclude(id=student.id).exists()
            if existing_roll_no:
                messages.error(request, "Roll number already exists. Please choose another.")
                return redirect('student_profile')  # Avoid saving if the roll number is already taken

        # Update the student details
        student.roll_no = roll_no  # Ensure roll_no is set
        student.name = name
        student.department = department
        student.year = year
        student.email = email
        student.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('student_profile')  # Avoid form resubmission on refresh

    # Fetch the student's attendance records
    attendance_records = Attendance.objects.filter(student=student).order_by("-date")

    return render(
        request,
        "student_profile.html",
        {
            "student": student,
            "attendance_records": attendance_records,
        },
    )


