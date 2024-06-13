from django.shortcuts import render,redirect
from .models import CustomUser, UserMember, Departments
from django.contrib.auth.models import User,auth
from django.contrib.auth import login,authenticate
from django.core.mail import send_mail
import random
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Assignment, Notification,Attendance,LeaveRequest,Project,Schedule
from django.urls import reverse
from django.db import IntegrityError
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import re

# Create your views here.
def index(request):
    return render(request,'index.html')
def aboutus(request):
    return render(request,'aboutus.html')

def loginpage(request):
    return render(request,'loginpage.html')
def career(request):
    return render(request,'career.html')
def contact(request):
    return render(request,'contact.html')

def signuptrainer(request):    
    departments = Departments.objects.all()
    return render(request,'signuptrainer.html',{'departments':departments})


def login1(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if user.user_type == '1':
                login(request,user)
                return redirect('admindash')
            elif user.user_type == '2':
                auth.login(request,user)
               
                return redirect('trainerdash')
            else:
                auth.login(request,user)
               
                return redirect('traineedash')
        else:
            messages.info(request,"invalid username or password")
            return redirect('loginpage')
    else:
        return redirect('loginpage')



def logout(request):
    return render(request,'index.html')
def generate_random_password():
    return str(random.randint(100000, 999999))


@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Trainee Manager').exists())
def approvedisapprove(request):
    departments = Departments.objects.all()
    users = UserMember.objects.filter(is_approved=False)
    
    countt = users.count()
    unapproved_leave_count = LeaveRequest.objects.filter(status='Pending')
    leavecount=unapproved_leave_count.count()
    return render(request, 'approvedisuser.html',{'users': users,'departments': departments,'coun': countt,'leavecount':leavecount})


@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Trainee Manager').exists())
def approve_user(request,pk):
    user_member = UserMember.objects.get( id=pk)
    approval_code = generate_random_password()
    user_member.is_approved = True
   
    user_member.user.set_password(approval_code)
    user_member.user.is_active = True
    user_member.user.save()
    user_member.save()

    # Send email with approval code
    send_mail(
       'Account Registration Confirmation',
        f'Hi {user_member.user.username} ,Your account has been created. Your password is: {approval_code}',
        'from@example.com',
        [user_member.user.email],
        fail_silently=False,
    )
    return redirect('approvedisapprove')

@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Trainee Manager').exists())
def disapprove_user(request,pk):
    user_member = UserMember.objects.get( id=pk)
    
    user_member.user.delete()
    user_member.delete()
    return redirect('approvedisapprove')
 # Ensure you have this utility function
def signuptrainer_db(request):
    errors = {}
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        contact = request.POST.get('contact')
        department_id = request.POST.get('department')
        image = request.FILES.get('image')
        certificate = request.FILES.get('certificate')
        password = generate_random_password()
        user_type = request.POST['text']

        # Email validation
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            errors['email'] = "Enter a valid email address."
        if CustomUser.objects.filter(email=email).exists():
            errors['email'] = "This email address already exists!"

        # Username validation
        if CustomUser.objects.filter(username=username).exists():
            errors['username'] = "This username already exists!"

        # Contact number validation
        contact_validator = RegexValidator(regex=r'^\+?\d{10,15}$', message="Enter a valid contact number.")
        try:
            contact_validator(contact)
        except ValidationError:
            errors['contact'] = "Enter a valid contact number."

        # Check if there are any errors
        if not errors:
            user1 = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                user_type=user_type,
                is_active=False  # User is inactive until admin approval
            )

            department = Departments.objects.get(id=department_id)

            member1 = UserMember(
                user=user1,
                department=department,
                contact=contact,
                image=image,
                certificates=certificate
            )
            member1.save()
            messages.success(request, 'Signup successful. Please wait for admin approval.')
            return redirect('signuptrainer')
        else:
            for field, error in errors.items():
                messages.error(request, error)

    else:
        first_name = last_name = email = username = contact = ''
        department_id = None
        image = certificate = None

    departments = Departments.objects.all()
    context = {
        'departments': departments,
        'errors': errors,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'username': username,
        'contact': contact,
        'department_id': department_id,
        'image': image,
        'certificate': certificate
    }
    return render(request, 'signuptrainer.html', context)

def signuptrainee(request):
    departments = Departments.objects.all()
    return render(request,'signuptrainee.html',{'departments': departments})
def signuptrainee_db(request): 
    
    errors = {}
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        contact = request.POST.get('contact')
        department_id = request.POST.get('department')
        image = request.FILES.get('image')
        certificate = request.FILES.get('certificate')
        password = generate_random_password()
        user_type = request.POST['text']

        # Email validation
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            errors['email'] = "Enter a valid email address."
        if CustomUser.objects.filter(email=email).exists():
            errors['email'] = "This email address already exists!"


        # Username validation
        if CustomUser.objects.filter(username=username).exists():
            errors['username'] = "This username already exists!"

        # Contact number validation
        contact_validator = RegexValidator(regex=r'^\+?\d{10,15}$', message="Enter a valid contact number.")
        try:
            contact_validator(contact)
        except ValidationError:
            errors['contact'] = "Enter a valid contact number."

        # Check if there are any errors
        if not errors:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                user_type=user_type,
                is_active=False  # User is inactive until admin approval
            )

            department = Departments.objects.get(id=department_id)

            member = UserMember(
                user=user,
                department=department,
                contact=contact,
                image=image,
                certificates=certificate
            )
            member.save()
            messages.success(request, 'Signup successful. Please wait for admin approval.')
            return redirect('signuptrainee')
        else:
            for field, error in errors.items():
                messages.error(request, error)

    else:
        first_name = last_name = email = username = contact = ''
        department_id = None
        image = certificate = None

    departments = Departments.objects.all()
    context = {
        'departments': departments,
        'errors': errors,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'username': username,
        'contact': contact,
        'department_id': department_id,
        'image': image,
        'certificate': certificate
    }
    return render(request, 'signuptrainee.html', context)
    


def adddepartment(request):
    users = UserMember.objects.filter(is_approved=False)
    
    countt = users.count()
    unapproved_leave_count = LeaveRequest.objects.filter(status='Pending')
    leavecount=unapproved_leave_count.count()
    return render(request,'adddepartment.html',{'coun':countt,'leavecount':leavecount})
def adddepartment_db(request):
    if request.method=='POST':
        departmentname=request.POST['departmentname']
        d=Departments(department_name=departmentname)
        d.save()
        messages.success(request, 'New department added successfully.')
        return redirect('adddepartment')
def admindash(request):
    users = UserMember.objects.filter(is_approved=False)
    unapproved_leave_count = LeaveRequest.objects.filter(status='Pending')
    leavecount=unapproved_leave_count.count()
    countt = users.count()
    return render(request,'admindash.html',{'coun':countt,'leavecount':leavecount})
def addtrainer(request):
    departments=Departments.objects.all()
    users = UserMember.objects.filter(is_approved=False)
    
    countt = users.count()
    unapproved_leave_count = LeaveRequest.objects.filter(status='Pending')
    leavecount=unapproved_leave_count.count()
    return render(request,'addtrainer.html',{'coun':countt,'departments':departments,'leavecount':leavecount})
def addtrainer_db(request):
    errors = {}
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        contact = request.POST.get('contact')
        department_id = request.POST.get('department')
        image = request.FILES.get('image')
        certificate = request.FILES.get('certificate')
        password = generate_random_password()
        user_type = request.POST['text']
        #approval_code = generate_random_password()

        # Email validation
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            errors['email'] = "Enter a valid email address."
        if CustomUser.objects.filter(email=email).exists():
            errors['email'] = "This email address already exists!"


        # Username validation
        if CustomUser.objects.filter(username=username).exists():
            errors['username'] = "This username already exists!"

        # Contact number validation
        contact_validator = RegexValidator(regex=r'^\+?\d{10,15}$', message="Enter a valid contact number.")
        try:
            contact_validator(contact)
        except ValidationError:
            errors['contact'] = "Enter a valid contact number."

        # Check if there are any errors
        if not errors:
            usera1 = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                user_type=user_type,
                is_active=True
                
                
                 # User is inactive until admin approval
                 # User is inactive until admin approval
            )

            department = Departments.objects.get(id=department_id)

            membera1 = UserMember(
                user=usera1,
                department=department,
                contact=contact,
                image=image,
                certificates=certificate,
                is_approved=True 
                 
                
            )
           
            membera1.save()
            messages.success(request, 'Reegistration successful.')
            send_mail(
                 'Account Registration Confirmation',
                  f'Hi {username} ,Your account has been created. Your password is: {password}',
                 'from@example.com',
                  [membera1.user.email],
                  fail_silently=False,
             )
            return redirect('addtrainer')
        else:
            for field, error in errors.items():
                messages.error(request, error)

    else:
        first_name = last_name = email = username = contact = ''
        department_id = None
        image = certificate = None

    departments = Departments.objects.all()
    context = {
        'departments': departments,
        'errors': errors,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'username': username,
        'contact': contact,
        'department_id': department_id,
        'image': image,
        'certificate': certificate
    }
       
    return render(request, 'addtrainer.html', context)



def addtrainee(request):
    departments=Departments.objects.all()
    users = UserMember.objects.filter(is_approved=False)
    
    countt = users.count()
    unapproved_leave_count = LeaveRequest.objects.filter(status='Pending')
    leavecount=unapproved_leave_count.count()
    return render(request,'addtrainee.html',{'coun':countt,'departments':departments,'leavecount':leavecount})
def addtrainee_db(request):
    errors = {}
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        contact = request.POST.get('contact')
        department_id = request.POST.get('department')
        image = request.FILES.get('image')
        certificate = request.FILES.get('certificate')
        password = generate_random_password()
        user_type = request.POST['text']
        #approval_code = generate_random_password()

        # Email validation
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            errors['email'] = "Enter a valid email address."
        if CustomUser.objects.filter(email=email).exists():
            errors['email'] = "This email address already exists!"


        # Username validation
        if CustomUser.objects.filter(username=username).exists():
            errors['username'] = "This username already exists!"

        # Contact number validation
        contact_validator = RegexValidator(regex=r'^\+?\d{10,15}$', message="Enter a valid contact number.")
        try:
            contact_validator(contact)
        except ValidationError:
            errors['contact'] = "Enter a valid contact number."

        # Check if there are any errors
        if not errors:
            usera = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                user_type=user_type,
                is_active=True
               
                 # User is inactive until admin approval
                 # User is inactive until admin approval
            )

            department = Departments.objects.get(id=department_id)

            membera = UserMember(
                user=usera,
                department=department,
                contact=contact,
                image=image,
                certificates=certificate,
                is_approved=True
            )
            membera.save()
            messages.success(request, 'Registration successful.')
            send_mail(
                   'Account Registration Confirmation',
                    f'Hi {username} ,Your account has been created. Your password is: {password}',
                    'from@example.com',
                    [membera.user.email],
                     fail_silently=False,
            )
            return redirect('addtrainee')
        else:
            for field, error in errors.items():
                messages.error(request, error)

    else:
        first_name = last_name = email = username = contact = ''
        department_id = None
        image = certificate = None

    departments = Departments.objects.all()
    context = {
        'departments': departments,
        'errors': errors,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'username': username,
        'contact': contact,
        'department_id': department_id,
        'image': image,
        'certificate': certificate
    }
    
    return render(request, 'addtrainee.html', context)


def viewtrainer(request):
    users = UserMember.objects.filter(is_approved=False)
    
    countt = users.count()
    unapproved_leave_count = LeaveRequest.objects.filter(status='Pending')
    leavecount=unapproved_leave_count.count()
    trainers = UserMember.objects.filter(user__user_type='2')
    return render(request, 'viewtrainer.html', {'trainers': trainers,'coun':countt,'leavecount':leavecount})
def delete_trainer(request,pk):
    trainer=UserMember.objects.get(id=pk)
    user = trainer.user
    trainer.delete()
    user.delete()
   
    return redirect('viewtrainer')



def viewtrainee(request):
    users = UserMember.objects.filter(is_approved=False)
    
    countt = users.count()
    unapproved_leave_count = LeaveRequest.objects.filter(status='Pending')
    leavecount=unapproved_leave_count.count()
    trainees = UserMember.objects.filter(user__user_type='3')
    return render(request, 'viewtrainee.html', {'trainees': trainees,'coun':countt,'leavecount':leavecount})
def delete_trainee(request,pk):
    trainee=UserMember.objects.get(id=pk)
    user = trainee.user
    trainee.delete()
    user.delete()
   
    return redirect('viewtrainee')
    

def leaverequestapprove(request):
     users=LeaveRequest.objects.all()
     userss = UserMember.objects.filter(is_approved=False)
     
     countt = userss.count()
     
     unapproved_leave_count = LeaveRequest.objects.filter(status='Pending')
     leavecount=unapproved_leave_count.count()
     return render(request, 'leaverequest.html',{'coun':countt,'users':users,'leavecount':leavecount})
def approve_leave(request, pk):
    if request.method == 'POST':
        user_member = LeaveRequest.objects.get(id=pk)
        user_member.status = 'Approved'  # Update status to Approved
        user_member.save()

        # Send email with approval notification
        send_mail(
            'Leave Request',
            f'Hi {user_member.user.username}, your leave request has been approved.',
            'from@example.com',
            [user_member.user.email],
            fail_silently=False,
        )
    return redirect('leaverequestapprove')  # Redirect to the leave request list view

def disapprove_leave(request, pk):
    if request.method == 'POST':
        user_member = LeaveRequest.objects.get(id=pk)
        user_member.status = 'Disapproved'  # Update status to Disapproved
        user_member.save()

        # Send email with disapproval notification
        send_mail(
            'Leave Request',
            f'Hi {user_member.user.username}, your leave request has been disapproved.',
            'from@example.com',
            [user_member.user.email],
            fail_silently=False,
        )
    return redirect('leaverequestapprove')  # Redirect to the leave request list view


def allocate(request):
   
        trainees = UserMember.objects.filter(user__user_type='3')
        trainers = UserMember.objects.filter(user__user_type='2')
        users = UserMember.objects.filter(is_approved=False)
    
        countt = users.count()
        unapproved_leave_count = LeaveRequest.objects.filter(status='Pending')
        leavecount=unapproved_leave_count.count()
        return render(request, 'allocate.html', {'coun': countt, 'trainees': trainees, 'trainers': trainers,'leavecount':leavecount})
   
def assign_trainer(request):
    if request.method == "POST":
        trainee_id = request.POST.get("trainee_id")  
        trainer_id = request.POST.get("trainer_id")  
        try:
            trainee = UserMember.objects.get(id=trainee_id)
            trainer = UserMember.objects.get(id=trainer_id)
            
           
            assignment, created = Assignment.objects.update_or_create(
                trainee=trainee,
                defaults={'trainer': trainer, 'status': 'Assigned'}
            )
            
            # Create a notification for the trainer
            Notification.objects.create(
                trainer=trainer,
                message=f"You have been assigned to trainee {trainee.user.first_name}."
            )
            
            messages.success(request, "Trainer assigned successfully!")
        except UserMember.DoesNotExist:
            messages.error(request, "User not found.")
        
        return redirect(reverse('allocate'))
def get_trainees(request, trainer_id):
    assignments = Assignment.objects.filter(trainer__id=trainer_id).select_related('trainee')
    trainees = [{'id': assignment.id, 'name': f"{assignment.trainee.user.first_name} {assignment.trainee.user.last_name}"} for assignment in assignments]
    return JsonResponse({'trainees': trainees})

@login_required
def class_schedule(request):
    trainers = UserMember.objects.filter(user__user_type='2')
    trainees = []
    selected_trainer_id = None
    users = UserMember.objects.filter(is_approved=False)
    
    countt = users.count()
    unapproved_leave_count = LeaveRequest.objects.filter(status='Pending')
    leavecount=unapproved_leave_count.count()
   
    if request.method == 'POST':
            selected_trainer_id = request.POST.get('trainer')
            if selected_trainer_id:
                trainees = Assignment.objects.filter(trainer__id=selected_trainer_id).select_related('trainee')
        
        
    return render(request, 'classschedule.html', {
            'coun': countt,
            'leavecount':leavecount,
            'trainers': trainers,
            'trainees': trainees,
            'selected_trainer_id': selected_trainer_id
        })
    

def addschedule_db(request):
    trainers = UserMember.objects.filter(user__user_type='2')
    trainees = []
    selected_trainer_id = None

    if request.method == 'POST':
        selected_trainer_id = request.POST.get('trainer')
        if selected_trainer_id:
            try:
                trainer_instance = UserMember.objects.get(id=selected_trainer_id)
                trainees = Assignment.objects.filter(trainer=trainer_instance).select_related('trainee')
            except ObjectDoesNotExist:
                return render(request, 'classschedule.html', {
                    'trainers': trainers,
                    'trainees': trainees,
                    'selected_trainer_id': selected_trainer_id,
                    'error_message': 'Selected trainer does not exist.'
                })
        
        if 'trainee' in request.POST:
            trainee_assignment_id = request.POST.get('trainee')
            day = request.POST.get('day')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')

            try:
                trainee_assignment = Assignment.objects.get(id=trainee_assignment_id)
                
                # Create and save the new schedule
                schedule = Schedule(
                    trainer=trainee_assignment,  # Use the Assignment instance
                    trainee=trainee_assignment,  # Use the Assignment instance
                    day=day,
                    start_time=start_time,
                    end_time=end_time
                )
                schedule.save()
                
                return redirect('class_schedule')
            except ObjectDoesNotExist:
                return render(request, 'classschedule.html', {
                    'trainers': trainers,
                    'trainees': trainees,
                    'selected_trainer_id': selected_trainer_id,
                    'error_message': 'Selected trainee assignment does not exist.'
                })

    return render(request, 'classschedule.html', {
        'trainers': trainers,
        'trainees': trainees,
        'selected_trainer_id': selected_trainer_id
    })

def trainerattendance(request):
     trainers=UserMember.objects.filter(user__user_type='2')
     users = UserMember.objects.filter(is_approved=False)
    
     countt = users.count()
     unapproved_leave_count = LeaveRequest.objects.filter(status='Pending')
     leavecount=unapproved_leave_count.count()
     return render(request, 'trainerattendance.html',{'coun':countt,'trainers':trainers,'leavecount':leavecount})

def addtrainer_attendance_db(request):
   

    if request.method == "POST":
        trainer = request.POST.get('trainer')
        date = request.POST.get('date')
        status = request.POST.get('status')
        
        trainer = UserMember.objects.get(id=trainer)
        attendance = Attendance(usermember=trainer, date=date, status=status)
        attendance.save()
        
        return redirect('trainerattendance')

def viewtrainerattendance(request):
     trainers=UserMember.objects.filter(user__user_type='2')
     users = UserMember.objects.filter(is_approved=False)
    
     countt = users.count()
     unapproved_leave_count = LeaveRequest.objects.filter(status='Pending')
     leavecount=unapproved_leave_count.count()
     return render(request, 'viewtrainerattendance.html',{'coun':countt,'trainers':trainers,'leavecount':leavecount})

def trainer_attendance_records(request):
    trainer_id = request.GET.get('trainer')
    start_date = request.GET.get('sdate')
    end_date = request.GET.get('edate')
    users = UserMember.objects.filter(is_approved=False)
    
    countt = users.count()
    unapproved_leave_count = LeaveRequest.objects.filter(status='Pending')
    leavecount=unapproved_leave_count.count()
    selected_trainer = UserMember.objects.get(id=trainer_id)
    attendance_records = Attendance.objects.filter(
        usermember=selected_trainer,
        date__range=[start_date, end_date]
    )

    context = {
        'attendance_records': attendance_records,
        'selected_trainer': selected_trainer,
        'start_date': start_date,
        'end_date': end_date,
        'coun':countt,
        'leavecount':leavecount
    }
    return render(request, 'trainer_attend_record.html', context)
def viewtraineeattendance(request):
    trainees = UserMember.objects.filter(user__user_type='3')
    users = UserMember.objects.filter(is_approved=False)
    
    countt = users.count()
    unapproved_leave_count = LeaveRequest.objects.filter(status='Pending')
    leavecount=unapproved_leave_count.count()
    return render(request, 'viewtrineeattendance.html', {'coun': countt, 'trainees': trainees,'leavecount':leavecount})

def trainee_attendance_records(request):
    trainee_id = request.GET.get('trainee')
    start_date = request.GET.get('sdate')
    end_date = request.GET.get('edate')
    users = UserMember.objects.filter(is_approved=False)
    
    countt = users.count()
    unapproved_leave_count = LeaveRequest.objects.filter(status='Pending')
    leavecount=unapproved_leave_count.count()
    # Handle case when parameters are missing
    if not (trainee_id and start_date and end_date):
        return redirect('viewtraineeattendance')  # Or render an error message

    selected_trainee = UserMember.objects.get(id=trainee_id)
    attendance_records = Attendance.objects.filter(
        usermember=selected_trainee,
        date__range=[start_date, end_date]
    )

    context = {
        'attendance_records': attendance_records,
        'selected_trainee': selected_trainee,
        'start_date': start_date,
        'end_date': end_date,
        'coun':countt,
        'leavecount':leavecount
    }
    return render(request, 'trainee_attendance_records.html', context)









def trainerdash(request):
    user_member= UserMember.objects.get(user=request.user)
   
    unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
    return render(request,'trainerdash.html',{'user_member':user_member,'unread_notifications_count': unread_notifications_count})
def edit_trainer(request, pk):
   
    user_member= UserMember.objects.get(user=request.user)
    unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
    return render(request,'edit_trainer.html',{'user_member':user_member,'unread_notifications_count': unread_notifications_count})
@login_required
def edit_trainer_db(request, pk):
    user_member =UserMember.objects.get(user=request.user)
    user = user_member.user
    errors = {}

    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        contact = request.POST.get('contact')

        # Email validation
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            errors['email'] = "Enter a valid email address."
        if CustomUser.objects.filter(email=email).exclude(pk=user.pk).exists():
            errors['email'] = "This email address already exists!"

        # Username validation
        if CustomUser.objects.filter(username=username).exclude(pk=user.pk).exists():
            errors['username'] = "This username already exists!"

        # Contact number validation
        contact_validator = RegexValidator(regex=r'^\+?\d{10,15}$', message="Enter a valid contact number.")
        try:
            contact_validator(contact)
        except ValidationError:
            errors['contact'] = "Enter a valid contact number."

        # Check if there are any errors
        if not errors:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user_member.contact = contact

            if 'image' in request.FILES:
                user_member.image = request.FILES['image']

            if 'certificate' in request.FILES:
                user_member.certificates = request.FILES['certificate']

            user.save()
            user_member.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('edit_trainer', pk=user_member.pk)
        else:
            for field, error in errors.items():
                messages.error(request, error)

    return render(request, 'edit_trainer.html', {'user_member': user_member, 'errors': errors})
@login_required
def notifications(request):
    user_member= UserMember.objects.get(user=request.user)
    try:
       
        notifications = Notification.objects.filter(trainer=user_member).order_by('-created_at')
        unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
        
        # Mark all notifications as read
        Notification.objects.filter(trainer=user_member, read=False).update(read=True)
        return render(request, 'notifications.html', {'notifications': notifications,'user_member':user_member,'unread_notifications_count': unread_notifications_count})
    except UserMember.DoesNotExist:
        return render(request, 'notifications.html', {'notifications': [],'unread_notifications_count': 0})
@login_required
def classschedule_trainer(request,trainer_id):
    user_member= UserMember.objects.get(user=request.user)
    trainer = UserMember.objects.get(id=trainer_id)
    assignments = Assignment.objects.filter(trainer=trainer)
    schedules = Schedule.objects.filter(trainer__in=assignments).select_related('trainee')
    unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()

    return render(request, 'schedule_trainer.html', {
        'trainer': trainer,
        'schedules': schedules,
        'user_member':user_member,
        'unread_notifications_count': unread_notifications_count
    })

@login_required
def applyleave_trainer(request):
     user_member= UserMember.objects.get(user=request.user)
     unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
     return render(request, 'applyleavetrainer.html', {'user_member':user_member,'unread_notifications_count':unread_notifications_count })
@login_required
def applyleavetrainer_db(request):
    if request.method == 'POST':
        fromdate = request.POST['fdate']
        todate = request.POST['tdate']
        reason = request.POST['reason']

       

    
        user_member = UserMember.objects.get(user=request.user)
        leave_request = LeaveRequest(
                user=request.user,
                department=user_member.department,
                start_date=fromdate,
                end_date=todate,
                reason=reason
            )
        leave_request.save()
        messages.success(request, 'Leave request submitted successfully.')
        return redirect('applyleave_trainer')
        

@login_required    
def assignproject(request):
     user_member= UserMember.objects.get(user=request.user)
     assignments = Assignment.objects.filter(trainer=user_member)
    # Get the assigned trainees from the assignments
     assigned_trainees = [assignment.trainee for assignment in assignments]
     unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
     return render(request, 'assignproject.html', {'user_member':user_member,'trainees': assigned_trainees,'unread_notifications_count': unread_notifications_count})
@login_required
def assignproject_db(request):
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        trainee_id = request.POST.get('trainee')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        trainee = UserMember.objects.get(id=trainee_id)
        trainer = UserMember.objects.get(user=request.user)
        assignment = Assignment.objects.get(trainer=trainer, trainee=trainee)

        project=Project.objects.create(
            assignment=assignment,
            name=project_name,
            start_date=start_date,
            end_date=end_date,
            status='Not Uploaded'
        )
        project.save()
        Notification.objects.create(
                trainer=trainee,
                message=f"Upload your project. Topic: {project_name}.",
               
                read=False
        )

        
        return redirect('assignproject')  # Redirect to a success page or the desired page after assignment

    return redirect('assignproject')  # Redirect back if the request method is not POST
@login_required
def viewproject(request):
   

    # Get the current logged-in user (trainer)
    user_member = UserMember.objects.get(user=request.user)
    
    # Get assignments where the logged-in user is the trainer
    assignments = Assignment.objects.filter(trainer=user_member)
    
    # Get the projects related to those assignments
    projects = Project.objects.filter(assignment__in=assignments)
    unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
    
    return render(request, 'viewproject.html', {'user_member': user_member, 'projects': projects,'unread_notifications_count':unread_notifications_count})

def owntrainerattendance(request):
    user_member = UserMember.objects.get(user=request.user)
    assignments = Assignment.objects.filter(trainer=user_member)
    # Get the assigned trainees from the assignments
    assigned_trainees = [assignment.trainee for assignment in assignments]
    unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
    return render(request, 'owntrainerattendance.html', {'trainees': assigned_trainees, 'user_member': user_member,'unread_notifications_count':unread_notifications_count}) 
def owntrainer_attendance_records(request):
    user_member = UserMember.objects.get(user=request.user)
    unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
    start_date = request.GET.get('sdate')
    end_date = request.GET.get('edate')

    # Handle case when parameters are missing
    if not (start_date and end_date):
        return redirect('owntrainerattendance')  # Or render an error message

    selected_trainer = UserMember.objects.get(user=request.user)
    attendance_records = Attendance.objects.filter(
        usermember=selected_trainer,
        date__range=[start_date, end_date]
    )
    
    context = {
        'attendance_records': attendance_records,
        'selected_trainer': selected_trainer,
        'start_date': start_date,
        'end_date': end_date,
        'user_member': user_member,
        'unread_notifications_count': unread_notifications_count
    }
    return render(request, 'owntrainerattendance_record.html', context)



def traineeattendance(request):
    user_member = UserMember.objects.get(user=request.user)
    assignments = Assignment.objects.filter(trainer=user_member)
    # Get the assigned trainees from the assignments
    assigned_trainees = [assignment.trainee for assignment in assignments]
    unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
    return render(request, 'traineeattendance.html', {'trainees': assigned_trainees, 'user_member': user_member,'unread_notifications_count':unread_notifications_count})

def addtrainee_attendance_db(request):
    if request.method == "POST":
        trainee_id = request.POST.get('trainee')
        date = request.POST.get('date')
        status = request.POST.get('status')

        trainee = UserMember.objects.get(id=trainee_id)
        attendance_trainee = Attendance(usermember=trainee, date=date, status=status)
        attendance_trainee.save()

        return redirect('traineeattendance')
def showtraineeattendance(request):
    user_member = UserMember.objects.get(user=request.user)
    assignments = Assignment.objects.filter(trainer=user_member)
    # Get the assigned trainees from the assignments
    assigned_trainees = [assignment.trainee for assignment in assignments]
    unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
    return render(request, 'showtraineeattendance.html', {'trainees': assigned_trainees, 'user_member': user_member,'unread_notifications_count':unread_notifications_count})


def showtrainee_attendancerecords(request):
    user_member = UserMember.objects.get(user=request.user)
    unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
    trainee_id = request.GET.get('trainee')
    start_date = request.GET.get('sdate')
    end_date = request.GET.get('edate')
    
    # Handle case when parameters are missing
    if not (trainee_id and start_date and end_date):
        return redirect('showtraineeattendance')  # Or render an error message

    selected_trainee = UserMember.objects.get(id=trainee_id)
    attendance_records = Attendance.objects.filter(
        usermember=selected_trainee,
        date__range=[start_date, end_date]
    )

    context = {
        'attendance_records': attendance_records,
        'selected_trainee': selected_trainee,
        'start_date': start_date,
        'end_date': end_date,
        'user_member': user_member,
        'unread_notifications_count':unread_notifications_count
    }
    return render(request, 'showtrainee_record.html', context)
def changepasswordtrainer(request):
     user_member= UserMember.objects.get(user=request.user)
     unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
    
     return render(request, 'changepasstrainer.html', {'user_member':user_member,'unread_notifications_count':unread_notifications_count})
@login_required
def changepasswordtrainer_db(request):
 

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        user = request.user

        def is_valid_password(password):
            if len(password) < 6:
                return "Password must be at least 6 characters long."
            if not re.search(r'[A-Z]', password):
                return "Password must contain at least one uppercase letter."
            if not re.search(r'[a-z]', password):
                return "Password must contain at least one lowercase letter."
            if not re.search(r'\d', password):
                return "Password must contain at least one number."
            if not re.search(r'[\W_]', password):
                return "Password must contain at least one special character."
            return None

        if user.check_password(old_password):
            if new_password1 == new_password2:
                validation_error = is_valid_password(new_password1)
                if validation_error:
                    messages.error(request, validation_error)
                else:
                    user.set_password(new_password1)
                    user.save()
                    #messages.success(request, 'Your password was successfully updated!,')
                    # Re-authenticate the user
                    user = authenticate(username=user.username, password=new_password1)
                    return redirect('loginpage')
            else:
                messages.error(request, 'New passwords do not match.')
        else:
            messages.error(request, 'Old password is incorrect.')

    # Fetch the same context variables as in changepasswordtrainee
    user_member = UserMember.objects.get(user=request.user)
    unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
    return render(request, 'changepasstrainer.html', {'user_member': user_member, 'unread_notifications_count': unread_notifications_count})
def traineedash(request):
    user_member= UserMember.objects.get(user=request.user)
    unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
    return render(request,'traineedash.html',{'user_member':user_member,'unread_notifications_count': unread_notifications_count})
def edit_trainee(request, pk):
   
    user_member= UserMember.objects.get(user=request.user)
    unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
    return render(request,'edit_trainee.html',{'user_member':user_member,'unread_notifications_count': unread_notifications_count})
@login_required
def edit_trainee_db(request, pk):
    
    user_member =UserMember.objects.get(user=request.user)
    user = user_member.user
    errors = {}

    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        contact = request.POST.get('contact')

        # Email validation
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            errors['email'] = "Enter a valid email address."
        if CustomUser.objects.filter(email=email).exclude(pk=user.pk).exists():
            errors['email'] = "This email address already exists!"

        # Username validation
        if CustomUser.objects.filter(username=username).exclude(pk=user.pk).exists():
            errors['username'] = "This username already exists!"

        # Contact number validation
        contact_validator = RegexValidator(regex=r'^\+?\d{10,15}$', message="Enter a valid contact number.")
        try:
            contact_validator(contact)
        except ValidationError:
            errors['contact'] = "Enter a valid contact number."

        # Check if there are any errors
        if not errors:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user_member.contact = contact

            if 'image' in request.FILES:
                user_member.image = request.FILES['image']

            if 'certificate' in request.FILES:
                user_member.certificates = request.FILES['certificate']

            user.save()
            user_member.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('edit_trainee', pk=user_member.pk)
        else:
            for field, error in errors.items():
                messages.error(request, error)

    return render(request, 'edit_trainee.html', {'user_member': user_member, 'errors': errors})
def notificationtrainee(request):
    user_member= UserMember.objects.get(user=request.user)
    try:
        trainee = UserMember.objects.get(user=request.user)
        notifications = Notification.objects.filter(trainer=trainee).order_by('-created_at')
        unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
        
        # Mark all notifications as read
        Notification.objects.filter(trainer=user_member, read=False).update(read=True)
        return render(request, 'notificationtrainee.html', {'notifications': notifications,'user_member':user_member,'unread_notifications_count':unread_notifications_count})
    except UserMember.DoesNotExist:
        return render(request, 'notificationtrainee.html', {'notifications': []})
def classschedule_trainee(request,trainee_id):
    user_member= UserMember.objects.get(user=request.user)
    trainee = UserMember.objects.get(id=trainee_id)
    assignments = Assignment.objects.filter(trainee=trainee)
    schedules = Schedule.objects.filter(trainer__in=assignments).select_related('trainer')
    unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()

    return render(request, 'schedule_trainee.html', {
        'trainee': trainee,
        'schedules': schedules,
        'user_member':user_member,
        'unread_notifications_count':unread_notifications_count
    })
def uploadproject(request):
    user_member = UserMember.objects.get(user=request.user)
    # Get assignments where the logged-in user is the trainer
    assignments = Assignment.objects.filter(trainee=user_member)
    # Get the projects related to those assignments
    projects = Project.objects.filter(assignment__in=assignments)
    unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
    return render(request, 'uploadproject.html', {'user_member': user_member, 'projects': projects,'unread_notifications_count':unread_notifications_count})


def uploadproject_db(request):
      if request.method == 'POST':
        project_id = request.POST.get('project_id')
        uploaded_file = request.FILES.get('file')
        
        # Ensure the project ID and file are provided
        if not project_id or not uploaded_file:
            return redirect('uploadproject')
        
        # Get the project to which the file should be uploaded
        project = Project.objects.get(id=project_id)
        
        # Save the uploaded file to the project's file field
        project.file = uploaded_file
        project.status = 'Uploaded'
        project.save()
        
        return redirect('uploadproject')  # Redirect to the upload project page
    
      return redirect('uploadproject')
@login_required
def applyleave_trainee(request):
     user_member= UserMember.objects.get(user=request.user)
     unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
     return render(request, 'applyleavetrainee.html', {'user_member':user_member,'unread_notifications_count':unread_notifications_count})
@login_required
def applyleavetrainee_db(request):
    if request.method == 'POST':
        fromdate = request.POST['fdate']
        todate = request.POST['tdate']
        reason = request.POST['reason']

       

    
        user_member = UserMember.objects.get(user=request.user)
        leave_request = LeaveRequest(
                user=request.user,
                department=user_member.department,
                start_date=fromdate,
                end_date=todate,
                reason=reason
            )
        leave_request.save()
        messages.success(request, 'Leave request submitted successfully.')
        return redirect('applyleave_trainee')
        

def owntraineeattendance(request):
    user_member = UserMember.objects.get(user=request.user)
    unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
    
    return render(request, 'owntraineeattendance.html', {'user_member': user_member,'unread_notifications_count':unread_notifications_count}) 
def owntrainee_attendance_records(request):
    user_member = UserMember.objects.get(user=request.user)
    unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
    
    start_date = request.GET.get('sdate')
    end_date = request.GET.get('edate')

    # Handle case when parameters are missing
    if not (start_date and end_date):
        return redirect('owntraineeattendance')  # Or render an error message

    selected_trainee = UserMember.objects.get(user=request.user)
    attendance_records = Attendance.objects.filter(
        usermember=selected_trainee,
        date__range=[start_date, end_date]
    )

    context = {
        'attendance_records': attendance_records,
        'selected_trainee': selected_trainee,
        'start_date': start_date,
        'end_date': end_date,
        'user_member': user_member,
        'unread_notifications_count':unread_notifications_count
    }
    return render(request, 'owntraineeattendance_records.html', context)



def changepasswordtrainee(request):
     user_member= UserMember.objects.get(user=request.user)
     unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
    
     return render(request, 'changepasswordtrainee.html', {'user_member':user_member,'unread_notifications_count':unread_notifications_count})
@login_required
def changepasswordtrainee_db(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        user = request.user

        def is_valid_password(password):
            if len(password) < 6:
                return "Password must be at least 6 characters long."
            if not re.search(r'[A-Z]', password):
                return "Password must contain at least one uppercase letter."
            if not re.search(r'[a-z]', password):
                return "Password must contain at least one lowercase letter."
            if not re.search(r'\d', password):
                return "Password must contain at least one number."
            if not re.search(r'[\W_]', password):
                return "Password must contain at least one special character."
            return None

        if user.check_password(old_password):
            if new_password1 == new_password2:
                validation_error = is_valid_password(new_password1)
                if validation_error:
                    messages.error(request, validation_error)
                else:
                    user.set_password(new_password1)
                    user.save()
                    #messages.success(request, 'Your password was successfully updated!')
                    # Re-authenticate the user
                    user = authenticate(username=user.username, password=new_password1)
                    return redirect('loginpage')
            else:
                messages.error(request, 'New passwords do not match.')
        else:
            messages.error(request, 'Old password is incorrect.')

    # Fetch the same context variables as in changepasswordtrainee
    user_member = UserMember.objects.get(user=request.user)
    unread_notifications_count = Notification.objects.filter(trainer=user_member, read=False).count()
    return render(request, 'changepasswordtrainee.html', {'user_member': user_member, 'unread_notifications_count': unread_notifications_count})