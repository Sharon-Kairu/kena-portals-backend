from rest_framework import serializers
from .models import Enrollment
from courses.models import Course, SubscriptionPlan

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','name', ]  

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', ] 

class EnrollmentSerializer(serializers.ModelSerializer):
    standalone_courses = CourseSerializer(many=True, read_only=True)
    subscription_courses = CourseSerializer(many=True, read_only=True)
    subscription_plan = SubscriptionPlanSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id',
            'mode',
            'standalone_courses',
            'subscription_plan',
            'subscription_courses',
        ]