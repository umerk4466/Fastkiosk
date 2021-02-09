from django.shortcuts import render
from Users.forms import Signup_Form, Signup_Student_Form
# import models
from Users.models import Profile, Role, Permission, Student_data

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required

# for ajax functions
from django.http import JsonResponse


# sign-up student user
def create_student(username, student_roll_no, course_name):
    # get user instace from username
    user = User.objects.get(username=username)
    # check if student role exists else make it
    if Role.objects.filter(name="Student").exists():
        # get student role instanse
        role = Role.objects.get(name="Student")
    else:
        permission = Permission.objects.create(name="Read_Write")
        permission.save()
        role = Role.objects.create(name="Student", permission=permission)
        role.save()
    # create student profile
    student_profile = Profile.objects.create(user=user, role=role)
    student_profile.save()
    # create student data model
    student_data = Student_data.objects.create(profile=student_profile,student_roll_no=student_roll_no,course_name=course_name )
    student_data.save()



# sign-up admin user
def create_admin(username):
    # get user instace from username
    user = User.objects.get(username=username)
    # check if student role exists else make it
    if Role.objects.filter(name="Admin").exists():
        # get student role instanse
        role = Role.objects.get(name="Admin")
    else:
        permission = Permission.objects.create(name="Full_Controll")
        permission.save()
        role = Role.objects.create(name="Admin", permission=permission)
        role.save()
    # create student profile
    student_profile = Profile.objects.create(user=user, role=role)
    student_profile.save()



# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = Signup_Form(request.POST)
        
        if form.is_valid():
            form.save()
            # Create profiles
            username = form.cleaned_data.get('username')
            # create admin profile function
            create_admin(username)
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        form = Signup_Form()
    return render(request, 'Users/signup.html', {'form': form})
    

def signup_student(request):
    if request.method == 'POST':
        form = Signup_Student_Form(request.POST)
        student_roll_no = request.POST.get('student_roll_no')
        course_name = request.POST.get('course_name')
        # check if this student roll no already exists
        if form.is_valid():
            if Student_data.objects.filter(student_roll_no=student_roll_no).exists():
                messages.error(request, 'Error!!! Student Roll Number already exists')
            else:
                form.save()
                # Create profiles
                username = form.cleaned_data.get('username')
                # create Student profile function
                create_student(username, student_roll_no, course_name)
                messages.success(request, 'Student Account created successfully')
                return redirect('login')
    else:
        form = Signup_Student_Form()
    return render(request, 'Users/signup_student.html', {'form': form})


# ajax functions
# to change student data ajax
@login_required
def ajax_change_student_data(request):
    course_name = request.GET.get('course_name', False)
    student_roll_no = request.GET.get('student_roll_no', False)
    cource_finish = request.GET.get('cource_finish', False)

    # get student data model id
    profile_id = Profile.objects.get(user=request.user.id)
    student_data = Student_data.objects.get(profile_id=profile_id.id)
    try:
        student_data.course_name = course_name
        student_data.student_roll_no = student_roll_no
        student_data.cource_finish = cource_finish
        student_data.save()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False})
    return JsonResponse(data)
