from django.db import models

# -------------------------------
# Register model (already in your project)
# -------------------------------
class Register(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=30, blank=False)
    email = models.CharField(max_length=25, blank=False, unique=True)
    phno = models.CharField(max_length=10, blank=False, unique=True)
    username = models.CharField(max_length=30, blank=False, unique=True)
    password = models.CharField(max_length=12, blank=False)
    role = models.CharField(max_length=20, blank=False)

    class Meta:
        db_table = "register_table"

# -------------------------------
# Student model
# -------------------------------
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    roll_no = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50)
    year = models.IntegerField()
    email = models.EmailField(unique=True)

    class Meta:
        db_table = "student_table"

    def __str__(self):
        return f"{self.roll_no} - {self.name}"

# -------------------------------
# Attendance model
# -------------------------------
class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])
    marked_by = models.CharField(max_length=50)  # teacher username

    class Meta:
        db_table = "attendance_table"

    def __str__(self):
        return f"{self.student.name} - {self.date} ({self.status})"
