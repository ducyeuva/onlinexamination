from django.urls import path,include
from django.contrib import admin
from exam import views
from django.contrib.auth.views import LogoutView,LoginView
urlpatterns = [
   
    path('admin/', admin.site.urls),
    path('student/',include('student.urls')),
    


    path('',views.home_view,name=''),
    path('logout', LogoutView.as_view(template_name='exam/logout.html'),name='logout'),
    path('contactus_view', views.contactus_view),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),



    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='exam/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),


    path('admin-student', views.admin_student_view,name='admin-student'),
    path('admin-view-student', views.admin_view_student_view,name='admin-view-student'),
    path('admin-view-student-marks', views.admin_view_student_marks_view,name='admin-view-student-marks'),
    path('admin-view-marks/<int:pk>', views.admin_view_marks_view,name='admin-view-marks'),
    path('admin-check-marks/<int:pk>', views.admin_check_marks_view,name='admin-check-marks'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    path('delete-student/<int:pk>', views.delete_student_view,name='delete-student'),

    path('admin-course', views.admin_course_view,name='admin-course'),
    path('admin-add-course', views.admin_add_course_view,name='admin-add-course'),
    path('admin-view-course', views.admin_view_course_view,name='admin-view-course'),
    path('admin-view-request/<int:course_id>/', views.admin_view_request, name='admin-view-request'),
    path('delete-course/<int:pk>', views.delete_course_view,name='delete-course'),

    path('admin-question', views.admin_question_view,name='admin-question'),
    path('admin-add-question', views.admin_add_question_view,name='admin-add-question'),
    path('admin-view-question', views.admin_view_question_view,name='admin-view-question'),
    path('view-question/<int:pk>', views.view_question_view,name='view-question'),
    path('view-all-question/<int:pk>', views.view_all_questions,name='view-all-question'),
    path('delete-question/<int:pk>', views.delete_question_view,name='delete-question'),


    path('add-exam-content-view', views.add_exam_content_view, name='add-exam-content-view'),
    path('view-exam-content-view', views.view_exam_content_view, name='add-exam-content-view'),
    path('view-delete-content/<int:course_id>/', views.view_delete_content, name='view-delete-content'),
    path('delete-content/<int:pk>/<int:course_id>/', views.delete_content, name='delete-content'),
    path('view-study-progress', views.view_study_progress, name='view-study-progress'),
    path('study-progress-view/<int:student_id>/', views.study_progress_view, name='study-progress-view'),
    path("views_student", views.views_student, name = "views_student"),
]
