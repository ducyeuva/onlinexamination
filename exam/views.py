from django.shortcuts import get_object_or_404, render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from student import models as SMODEL
from student import forms as SFORM
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Count
from .forms import ExamContentForm
from .models import ExamContent
from .models import StudyProgress
from .models import  Student




def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'exam/index.html')

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()
 

def afterlogin_view(request):
    if is_student(request.user):      
        return redirect('student/student-dashboard')
    else:
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_course':models.Course.objects.all().count(),
    'total_question':models.Question.objects.all().count(),
    }
    return render(request,'exam/admin_dashboard.html',context=dict)




@login_required(login_url='adminlogin')
def admin_student_view(request):
    dict={
        'total_student':SMODEL.Student.objects.all().count(),
    }
    return render(request,'exam/admin_student.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student.html',{'students':students})



@login_required(login_url='adminlogin')
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
    return render(request,'exam/update_student.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student')


@login_required(login_url='adminlogin')
def admin_course_view(request):
    return render(request,'exam/admin_course.html')


@login_required(login_url='adminlogin')
def admin_add_course_view(request):
    courseForm=forms.CourseForm()
    if request.method=='POST':
        courseForm=forms.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-course')
    return render(request,'exam/admin_add_course.html',{'courseForm':courseForm})


@login_required(login_url='adminlogin')
def admin_view_course_view(request):
    courses = models.Course.objects.all()
    return render(request,'exam/admin_view_course.html',{'courses':courses})

@login_required(login_url='adminlogin')
def delete_course_view(request,pk):
    course=models.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-view-course')



@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request,'exam/admin_question.html')


@login_required(login_url='adminlogin')
def admin_add_question_view(request):
    questionForm=forms.QuestionForm()
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=models.Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
        else: 
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-question')
    return render(request,'exam/admin_add_question.html',{'questionForm':questionForm})


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    courses= models.Course.objects.all()
    return render(request,'exam/admin_view_question.html',{'courses':courses})

@login_required(login_url='adminlogin')
def view_question_view(request,pk):
    questions=models.Question.objects.all().filter(course_id=pk)
    return render(request,'exam/view_question.html',{'questions':questions})

@login_required(login_url='adminlogin')
def delete_question_view(request,pk):
    question=models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')

@login_required(login_url='adminlogin')
def admin_view_student_marks_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student_marks.html',{'students':students})

@login_required(login_url='adminlogin')
def admin_view_marks_view(request,pk):
    courses = models.Course.objects.all()
    response =  render(request,'exam/admin_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response


#Xem điểm
@login_required(login_url='adminlogin')
def admin_check_marks_view(request,pk):
    course = models.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)
    results= models.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'exam/admin_check_marks.html',{'results':results})
    


def aboutus_view(request):
    return render(request,'exam/aboutus.html')

#Trang liên hệ
def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'exam/contactussuccess.html')
    return render(request, 'exam/contactus.html', {'form':sub})

#Xem mức độ YCCĐ
@login_required(login_url='adminlogin')
def admin_view_request(request, course_id):
    # Lấy đối tượng Course
    course_instance = models.Course.objects.get(id=course_id)

    # Tạo một dictionary để lưu tổng số câu hỏi cho mỗi mức độ khó khăn
    difficulty_data = {
        'biet': course_instance.question_set.filter(difficulty_level='biet').count(),
        'hieu': course_instance.question_set.filter(difficulty_level='hieu').count(),
        'van_dung_thap': course_instance.question_set.filter(difficulty_level='van_dung_thap').count(),
        'van_dung_cao': course_instance.question_set.filter(difficulty_level='van_dung_cao').count(),
    }
    return render(request, 'exam/admin_view_request.html', {'course_instance': course_instance, 'difficulty_data': difficulty_data})


@login_required(login_url='adminlogin')
def view_all_questions(request, course_id):
    # Lấy đối tượng Course
    course_instance = models.Course.objects.get(id=course_id)

    # Lấy tất cả câu hỏi của khóa học
    questions = models.Question.objects.filter(course=course_instance)

    # Truyền câu hỏi và đánh giá vào template
    return render(request, 'exam/view_all_questions.html', {'course_instance': course_instance, 'questions': questions})

# Thêm YCCĐ vào start exam
@login_required(login_url='adminlogin')
def add_exam_content_view(request):
    examcontentForm = ExamContentForm()
    if request.method == 'POST':
        examcontentForm = ExamContentForm(request.POST)
        if examcontentForm.is_valid():
            content = examcontentForm.save(commit=False)
            course_id = request.POST.get('courseID')  # Lấy course_id từ POST data
            course = models.Course.objects.get(id=course_id)
            content.course = course
            content.save()
            return HttpResponseRedirect('/admin-view-question')  # Chuyển hướng đến trang danh sách câu hỏi
        else:
            print("Form is invalid")

    return render(request, 'exam/add_exam_content_view.html', {'examcontentForm': examcontentForm})

#Xem YCCĐ
@login_required(login_url='adminlogin')
def view_exam_content_view(request):
    contents= models.ExamContent.objects.all()
    courses= models.Course.objects.all()
    return render(request,'exam/view_exam_content_view.html',{'contents':contents,'courses': courses})

#Xem trang YCCĐ để xóa
@login_required(login_url='adminlogin')
def view_delete_content(request, course_id):
    # Lấy đối tượng Course
    course_instance = models.Course.objects.get(id=course_id)
    # Truy vấn tất cả các bản ghi từ mô hình ExamContent, lọc theo course.
    contents=models.ExamContent.objects.filter(course = course_instance)
    return render(request, 'exam/view_delete_content.html', {'contents': contents,'course_instance': course_instance})

#xóa YCCĐ
@login_required(login_url='adminlogin')
def delete_content(request, pk, course_id):
    # Sử dụng get_object_or_404 để tránh lỗi nếu không tìm thấy bản ghi
    content = get_object_or_404(ExamContent, id=pk)
    content.delete()
    return redirect("view-delete-content", course_id)



@login_required(login_url='adminlogin')
def view_study_progress(request):
    progresses= models.StudyProgress.objects.all()
    students= SMODEL.Student.objects.all()
    return render(request,'exam/study_progress_view.html',{'progresses':progresses,'students': students})


@login_required(login_url='adminlogin')
def study_progress_view(request, student_id): # tiến trình vủa mỗi em học sinh
    student = SMODEL.Student.objects.get(id=student_id)
    courses = models.Course.objects.all()
    progress_data = []
    for course in courses:
        progress, created = StudyProgress.objects.get_or_create(student=student, course=course)
        progress_data.append({
            'course': course,
            'progress': progress,
        })
 
    return render(request, 'exam/study_progress_view.html', {'student': student, 'progress_data': progress_data})


@login_required(login_url='adminlogin')
def views_student(request):
    students = models.StudyProgress.objects.all()
    print("students", students)
    return render(request, 'exam/study_progress_view.html', {"students" : students})