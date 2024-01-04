from django.contrib import admin

from student.models import *
# Register your models here.
class AdminStudent(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', "mobile")
    list_filter = ('id', 'user', 'address', "mobile")

admin.site.register(Student, AdminStudent)