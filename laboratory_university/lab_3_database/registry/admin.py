# posts/admin.py

from django.contrib import admin
from .models import Course, Student, StudentCourse

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'credits', 'created_at']
    list_filter = ['credits', 'created_at']
    search_fields = ['course_name']
    ordering = ['course_name']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'birth_date', 'enrollment_date']
    list_filter = ['enrollment_date', 'birth_date']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['last_name']


@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'grade', 'enrollment_date']
    list_filter = ['course', 'grade']
    search_fields = ['student__last_name', 'student__first_name', 'course__course_name']
    ordering = ['-enrollment_date']