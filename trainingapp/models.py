from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class CustomUser(AbstractUser):
    user_type = models.CharField(default=1, max_length=10)
   

class Departments(models.Model):
    department_name = models.CharField(max_length=255, null=True)

class UserMember(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,related_name='usermember')
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=255, null=True)
    image = models.ImageField(blank=True, upload_to='image/', null=True)
    certificates = models.FileField(blank=True, null=True, upload_to='certificates/')
    is_approved = models.BooleanField(default=False)
    #status = models.CharField(max_length=20, default='Pending')


    
class Assignment(models.Model):
    trainee = models.ForeignKey(UserMember, related_name='trainee_assignments', on_delete=models.CASCADE)
    trainer = models.ForeignKey(UserMember, related_name='trainer_assignments', on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

class Notification(models.Model):
    trainer = models.ForeignKey(UserMember, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
class Attendance(models.Model):
    usermember= models.ForeignKey(UserMember, on_delete=models.CASCADE, null=True)
    date=models.DateField()
    status=models.TextField(max_length=10)
class LeaveRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default='Pending') 
class Schedule(models.Model):
    trainer = models.ForeignKey(Assignment, related_name='trainer_schedules', on_delete=models.CASCADE)
    trainee = models.ForeignKey(Assignment, related_name='trainee_schedules', on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    updated_at = models.DateTimeField(auto_now=True)

class Project(models.Model):
    
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='project_files/', blank=True, null=True)
    status= models.CharField(max_length=20, default='Not Uploaded') 



    