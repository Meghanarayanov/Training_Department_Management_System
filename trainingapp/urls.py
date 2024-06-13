from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
   path('',views.index,name='index'),
   path('aboutus',views.aboutus,name='aboutus'),
   path('career',views.career,name='career'),
   path('contact',views.contact,name='contact'),
   

   path('loginpage',views.loginpage,name='loginpage'),
   path('login1',views.login1,name='login1'),
   path('logout',views.logout,name='logout'),

   
   
   path('signuptrainer',views.signuptrainer,name='signuptrainer'),
   path('signuptrainer_db',views.signuptrainer_db,name='signuptrainer_db'),

   path('signuptrainee',views.signuptrainee,name='signuptrainee'),
   path('signuptrainee_db',views.signuptrainee_db,name='signuptrainee_db'),

  
  path('admindash',views.admindash,name='admindash'),
  path('adddepartment',views.adddepartment,name='adddepartment'),
  path('adddepartment_db',views.adddepartment_db,name='adddepartment_db'),
  path('addtrainer',views.addtrainer,name='addtrainer'),
  path('addtrainer_db',views.addtrainer_db,name='addtrainer_db'),
  path('addtrainee',views.addtrainee,name='addtrainee'),
  path('addtrainee_db',views.addtrainee_db,name='addtrainee_db'),
  path('viewtrainee',views.viewtrainee,name='viewtrainee'),
  path('viewtrainer',views.viewtrainer,name='viewtrainer'),
  path('delete_trainer/<int:pk>',views.delete_trainer,name='delete_trainer'),
  path('delete_trainee/<int:pk>',views.delete_trainee,name='delete_trainee'),
  path('approvedisapprove',views.approvedisapprove,name='approvedisapprove'),
  path('approve_user/<int:pk>', views.approve_user, name='approve_user'),
  path('disapprove_user/<int:pk>', views.disapprove_user, name='disapprove_user'),
  path('leaverequestapprove',views.leaverequestapprove,name='leaverequestapprove'),
  path('approve_leave/<int:pk>',views.approve_leave,name='approve_leave'),
  path('disapprove_leave/<int:pk>',views.disapprove_leave,name='disapprove_leave'),
  path('allocate',views.allocate,name='allocate'),
  path('assign_trainer',views.assign_trainer,name='assign_trainer'),
  path('class_schedule',views.class_schedule,name='class_schedule'),
  path('addschedule_db',views.addschedule_db,name='addschedule_db'),
  path('get_trainees/<int:trainer_id>/', views.get_trainees, name='get_trainees'),

  path('trainerattendance',views.trainerattendance,name='trainerattendance'),
  path('addtrainer_attendance_db',views.addtrainer_attendance_db,name='addtrainer_attendance_db'),
  
  path('viewtrainerattendance',views.viewtrainerattendance,name='viewtrainerattendance'),
  path('trainer_attendance_records',views. trainer_attendance_records, name='trainer_attendance_records'),
  path('viewtraineeattendance',views.viewtraineeattendance,name='viewtraineeattendance'),
  path('trainee_attendance_records',views. trainee_attendance_records, name='trainee_attendance_records'),


  
  



  path('trainerdash',views.trainerdash,name='trainerdash'),
  path('edit_trainer/<int:pk>',views.edit_trainer,name='edit_trainer'),
  path('edit_trainer_db/<int:pk>',views.edit_trainer_db,name='edit_trainer_db'),
  
  path('notifications',views.notifications,name='notifications'),
  path('classschedule_trainer/<int:trainer_id>',views.classschedule_trainer,name="classschedule_trainer"),

  path('applyleave_trainer',views.applyleave_trainer,name="applyleave_trainer"),
  path('applyleavetrainer_db',views.applyleavetrainer_db,name="applyleavetrainer_db"),
  path('assignproject',views.assignproject,name='assignproject'),
  path('assignproject_db',views.assignproject_db,name='assignproject_db'),
  path('viewproject',views.viewproject,name='viewproject'),

  path('owntrainerattendance',views.owntrainerattendance,name='owntrainerattendance'),
  path('owntrainer_attendance_records',views.owntrainer_attendance_records,name='owntrainer_attendance_records'),
  path('traineeattendance',views.traineeattendance,name='traineeattendance'),
  path('addtrainee_attendance_db',views.addtrainee_attendance_db,name='addtrainee_attendance_db'),
  path('showtraineeattendance',views.showtraineeattendance,name='showtraineeattendance'),
  path('showtrainee_attendancerecords',views. showtrainee_attendancerecords, name='showtrainee_attendancerecords'),
  path('changepasswordtrainer',views.changepasswordtrainer,name='changepasswordtrainer'),
  path('changepasswordtrainer_db',views.changepasswordtrainer_db,name='changepasswordtrainer_db'),


  

  
  path('traineedash',views.traineedash,name='traineedash'),
  path('edit_trainee/<int:pk>',views.edit_trainee,name='edit_trainee'),
  path('edit_trainee_db/<int:pk>',views.edit_trainee_db,name='edit_trainee_db'),
  
  path('notificationtrainee',views.notificationtrainee,name='notificationtrainee'),
  path('classschedule_trainee/<int:trainee_id>',views.classschedule_trainee,name="classschedule_trainee"),

  
  path('uploadproject',views.uploadproject,name='uploadproject'),
  path('uploadproject_db',views.uploadproject_db,name='uploadproject_db'),

  path('applyleave_trainee',views.applyleave_trainee,name="applyleave_trainee"),
  path('applyleavetrainee_db',views.applyleavetrainee_db,name="applyleavetrainee_db"),
  path('owntraineeattendance',views.owntraineeattendance,name='owntraineeattendance'),
  path('owntrainee_attendance_records',views.owntrainee_attendance_records,name='owntrainee_attendance_records'),
  path('changepasswordtrainee',views.changepasswordtrainee,name='changepasswordtrainee'),
  path('changepasswordtrainee_db',views.changepasswordtrainee_db,name='changepasswordtrainee_db'),
 


  
  
 



]