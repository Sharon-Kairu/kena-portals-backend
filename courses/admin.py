from django.contrib import admin
from .models import Course, Module, SubscriptionPlan

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0 

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'course', 'order']

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    filter_horizontal = ['included_courses']


