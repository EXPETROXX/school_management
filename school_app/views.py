from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login as auth_login,logout
from .models import *
from .models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

#login page
def login_page(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username = username,password = password)
        if user is not None and user.is_superuser ==True:
            auth_login(request,user)
            request.session['admin_id'] = user.id
            return redirect('admin_page')
        elif user is not None and user.user_type == 'student' and user.is_active == True:
            auth_login(request,user)
            request.session['stud_id'] =user.id
            return redirect('student_profile')
        elif user is not None and user.user_type =='teacher' and user.is_active == True:
            auth_login(request,user)
            request.session['teach_id'] =user.id
            return redirect('teacher_profile')
        else:
            return render(request,'login.html')

#logout
def log_out(request):
    logout(request)
    request.session.flush()
    return redirect('login_page')

#admin page
@login_required(login_url='login_page')  
def admin_page(request):
    if not request.user.is_superuser:
        return redirect('login_page')
    return render(request,'admin_page.html')

#depaertment register and view
@login_required(login_url='login_page')
def register_department(request):
    if not request.user.is_superuser:
        return redirect('login_page')
    if request.method == 'GET':
        dept_data = Department.objects.all()
        return render(request, 'register_department.html',{'dept_data':dept_data})
    else  :
        dep = request.POST['dept']
        data = Department.objects.create(department_name = dep)
        return redirect('register_department')

#delete department
@login_required(login_url='login_page')
def delete_department(request,id):
    if not request.user.is_superuser:
        return redirect('login_page')
    dept_data = Department.objects.get(id=id)
    dept_data.delete()
    return redirect('register_department')

#aprove student
@login_required(login_url='login_page')
def admin_student_view(request):
    if not request.user.is_superuser:
        return redirect('login_page')
    if request.GET.get('approve'):
        student_id = request.GET.get('approve')
        stud = Student.objects.get(id=student_id)
        stud.student_id.is_active = True
        stud.student_id.save()
        return redirect('admin_student_view')
    if request.GET.get('reject'):
        student_id = request.GET.get('reject')
        stud = Student.objects.get(id=student_id)
        user= stud.student_id
        stud.delete()
        user.delete()
        return redirect('admin_student_view')
    if request.GET.get('delete'):
        student_id = request.GET.get('delete')
        stud = Student.objects.get(id=student_id)
        user= stud.student_id
        stud.delete()
        user.delete()
        return redirect('admin_student_view')
    data = Student.objects.all()
    return render(request,"admin_student_view.html",{'data':data})

#approve teacher
@login_required(login_url='login_page')
def admin_teacher_view(request):
    if not request.user.is_superuser:
        return redirect('login_page')
    if request.GET.get('approve'):
        teacher_id = request.GET.get('approve')
        teach = Teacher.objects.get(id=teacher_id)
        teach.teacher_id.is_active = True
        teach.teacher_id.save()
        return redirect('admin_teacher_view')
    if request.GET.get('reject'):
        teacher_id = request.GET.get('reject')
        teach = Teacher.objects.get(id = teacher_id)
        user = teach.teacher_id
        teach.delete()
        user.delete()
        return redirect('admin_teacher_view')
    if request.GET.get('delete'):
        teacher_id = request.GET.get('delete')
        teach = Teacher.objects.get(id = teacher_id)
        user = teach.teacher_id 
        teach.delete()
        user.delete()
        return redirect('admin_teacher_view')
    data = Teacher.objects.all
    return render(request,"admin_teacher_view.html",{'data':data})

#register student
def register_student(request):
    if request.method == 'GET':
        data = Department.objects.all()
        return render(request, 'register_student.html', {'data': data})
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        department = request.POST.get('department')
        admission_number = request.POST.get('admission_number')
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        if User.objects.filter(username=user_name).exists():
            return HttpResponse("Username already exists. Please choose another username.")

        user_data = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=user_name,
            user_type='student',
            is_active=False  
        )
        user_data.set_password(password)
        user_data.save()

        # Create student record
        student_data = Student.objects.create(
            age=age,
            phone=phone,
            admission_number=admission_number,
            department_id_id=department,
            student_id_id=user_data.id
        )
        student_data.save()

        return HttpResponse("Registration successful! Please wait for admin approval.")

#register teacher
def register_teacher(request):
    if request.method =='GET':
        dept = Department.objects.all()
        return render(request,'register_teacher.html',{'dept':dept})
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        department = request.POST.get('department')
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        
        if User.objects.filter(username=user_name).exists():
            return HttpResponse("Username already exists. Please choose another username.")
        
        user_data = User.objects.create(first_name = first_name,
                                        last_name = last_name,
                                        email = email,
                                        username = user_name,
                                        user_type = 'teacher',
                                        is_active = False)
        user_data.set_password(password)
        user_data.save()

        teacher_data = Teacher.objects.create(phone = phone,
                                              age = age,
                                              department_id_id = department,
                                              teacher_id_id  = user_data.id )
        teacher_data.save()
        return HttpResponse("Registration successful! Please wait for admin approval.")

#student_profile
@login_required(login_url='login_page')  
def student_profile(request):
    if request.user.user_type != 'student':
        return redirect('login_page')
    data =  Student.objects.filter(student_id = request.user)
    return render(request,'student_profile.html',{'data':data})

# student_profile_edit
@login_required(login_url='login_page')
def student_profile_edit(request):
    # Ensure only students can access
    if request.user.user_type != 'student':
        return redirect('login_page')

    # Safely get the logged-in student's record
    student = get_object_or_404(Student, student_id=request.user)

    if request.method == 'GET':
        return render(request, 'student_profile_edit.html', {
            'student': student,
        })

    elif request.method == 'POST':
        # Update Student model
        student.phone = request.POST.get('phone') or 0
        student.age = request.POST.get('age') or 0
        student.save()

        # Update User model fields
        request.user.first_name = request.POST.get('first_name') or ''
        request.user.last_name = request.POST.get('last_name') or ''
        request.user.email = request.POST.get('email') or ''
        request.user.save()

        return redirect('student_profile')

# teacher page
@login_required(login_url='login_page')
def teacher_profile(request):
    if request.user.user_type != 'teacher':
        return redirect('login_page')
    teacher = get_object_or_404(Teacher, teacher_id=request.user)
    students = Student.objects.filter(department_id=teacher.department_id)
    return render(request, 'teacher_profile.html', {'teacher': teacher,'students': students,})

# edit teacher
@login_required(login_url='login_page')
def teacher_profile_edit(request):
    if request.user.user_type != 'teacher':
        return redirect('login_page')
    teacher = get_object_or_404(Teacher, teacher_id=request.user)
    if request.method == 'GET':
        return render(request,'teacher_profile_edit.html',{'teacher':teacher})
    elif request.method =='POST':

        # update Teacher model
        teacher.phone = request.POST.get('phone') or 0
        teacher.age = request.POST.get('age') or 0
        teacher.save()

        # update User model
        request.user.first_name = request.POST.get('first_name') or " "
        request.user.last_name = request.POST.get('last_name') or " "
        request.user.email = request.POST.get('email') or " "
        request.user.save()
        return redirect('teacher_profile')
    return