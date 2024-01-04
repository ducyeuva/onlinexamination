from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from django.contrib.auth.models import User
from .models import  Student
from django.shortcuts import get_object_or_404

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    print(QMODEL.Student.objects.all())
    dict={
    "student": QMODEL.Student.objects.get(user = User.objects.get(id = request.user.id)),
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    }
    return render(request,'student/student_dashboard.html',context=dict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_exam.html',{'courses':courses})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    questions=QMODEL.Question.objects.all().filter(course=course)
    if request.method=='POST':
        pass
    response= render(request,'student/start_exam.html',{'course':course,'questions':questions})
    response.set_cookie('course_id',course.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)  
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):     #duyệt câu hỏi
            selected_ans = request.COOKIES.get(str(i+1)) 
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        progress = QMODEL.StudyProgress()
        progress.student = student 
        progress.course = course 
        count_questions = QMODEL.Question.objects.filter(course = course).count() 
        progress.progress_percentage = total_marks/count_questions * 100
        progress.save()
        # 10c 1d 10d
        # 8d totalma
        #  8/10 * 100
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.save()
        return HttpResponseRedirect('view-result') 



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})
    
  
login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'student/check_marks.html',{'results':results})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_marks.html',{'courses':courses})



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_detail_view(request, result_id):
    result = QMODEL.Result.objects.get(id=result_id)

    # Lấy danh sách câu hỏi của bài kiểm tra
    questions = QMODEL.Question.objects.filter(course=result.exam)
    # Lấy các câu trả lời đã chọn bởi sinh viên
    selected_answers =[]
    for i in range(len(questions)):     #duyệt câu hỏi
        selected_answers.append(request.COOKIES.get(str(i+1)))  
    # Tạo danh sách chứa thông tin chi tiết về từng câu hỏi
    question_details = []
    count = 0 
    for question in questions:
        is_correct = question.answer == selected_answers[count]
        #Hiện nội dung từng option
        correct_answer = None
        if question.answer == "Option1":
            correct_answer = question.option1
        elif question.answer == "Option2":
            correct_answer = question.option2
        elif question.answer == "Option3":
            correct_answer = question.option3
        elif question.answer == "Option4":
            correct_answer = question.option4
        selected_answer = None
        if selected_answers[count] == "Option1":
            selected_answer = question.option1
        elif selected_answers[count] == "Option2":
            selected_answer = question.option2
        elif selected_answers[count] == "Option3":
            selected_answer = question.option3
        elif selected_answers[count] == "Option4":
            selected_answer = question.option4
        question_details.append({
            'question_text': question.question,
            'selected_answer': selected_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct,
        })
        count += 1

    # Truyền thông tin chi tiết vào template để hiển thị
    context = {
        'result': result,
        'question_detastudentloginils': question_details,
    }

    return render(request, 'student/view_result_detail.html', context)



@login_required(login_url='studentlogin') 
def study_progress_student(request, student_id): # tiến trình vủa mỗi em học sinh
    student = models.Student.objects.get(id=student_id)
    courses = QMODEL.Course.objects.all()
    progress_data = []
    for course in courses:
        progress, created = QMODEL.StudyProgress.objects.get_or_create(student=student, course=course)
        progress_data.append({
            'course': course,
            'progress': progress,
        })
    print("progress_data", progress_data)

    return render(request, 'student/study_progress.html', {'student': student, 'progress_data': progress_data})