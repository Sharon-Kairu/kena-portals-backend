from rest_framework import serializers
from .models import Request
from courses.models import Course

class RequestSerializer(serializers.ModelSerializer):
    course = serializers.CharField()  # Accept course name as string
    student_name = serializers.SerializerMethodField()
    student_id = serializers.SerializerMethodField()
    
    class Meta:
        model = Request
        fields = ['id', 'student_name', 'student_id', 'course', 'request_date', 
                  'request_time', 'request_reason', 'date_posted', 'status']
        read_only_fields = ['id', 'student_name', 'student_id', 'date_posted', 'status']

    def get_student_name(self, obj):
        return f"{obj.student.user.first_name} {obj.student.user.last_name}"
    
    def get_student_id(self, obj):
        return obj.student.student_id

    def create(self, validated_data):
        # Get course name and look up the Course object
        course_name = validated_data.pop('course')
        try:
            course = Course.objects.get(name=course_name)
        except Course.DoesNotExist:
            raise serializers.ValidationError({"course": f"Course '{course_name}' not found."})
        
        # Create the Request with the Course object
        validated_data['course'] = course
        return Request.objects.create(**validated_data)
    
    def to_representation(self, instance):
        # For reading, show course name
        representation = super().to_representation(instance)
        if instance.course:
            representation['course'] = instance.course.name
        return representation

        