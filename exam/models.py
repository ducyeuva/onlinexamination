from django.db import models
from student.models import Student
from django.utils import timezone
class Course(models.Model):
   course_name = models.CharField(max_length=50)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   exam_requirement = models.TextField(blank=True, null=True)  # Thêm trường mới để lưu nội dung cần đạt
   def __str__(self):
        return self.course_name

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    DIFFICULTY_CHOICES= [
        ('biet', 'Biết'),
        ('hieu', 'Hiểu'),
        ('van_dung_thap', 'Vận dụng thấp'),
        ('van_dung_cao', 'Vận dụng cao'),
    ]
    answer=models.CharField(max_length=200,choices=cat)
    difficulty_level= models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='biet')

class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

class ExamContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Khóa học')
    exam_requirement = models.TextField()

    def __str__(self):
        return f"{self.course.course_name} - Yêu cầu kỳ thi"


class StudyProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress_percentage = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.course_name} - {self.progress_percentage}%"