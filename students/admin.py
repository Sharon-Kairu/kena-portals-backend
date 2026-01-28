from django.contrib import admin
from .models import Student, StudentModule

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'get_full_name', 'get_email', 'payment_status', 'total_fees')
    list_filter = ('payment_status',)
    search_fields = ('student_id', 'user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('student_id',)
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Name'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


@admin.register(StudentModule)
class StudentModuleAdmin(admin.ModelAdmin):
    list_display = ('get_student_id', 'get_student_name', 'module', 'status', 'date_graded', 'comment')
    list_filter = ('status', 'comment')
    search_fields = ('student__student_id', 'student__user__first_name', 'module__title')
    
    def get_student_id(self, obj):
        return obj.student.student_id
    get_student_id.short_description = 'Student ID'
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    get_student_name.short_description = 'Student Name'