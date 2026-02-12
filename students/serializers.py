from rest_framework import serializers
from .models import Student, StudentModule
from users.serializer import UserSerializer
from users.models import User


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    student_id = serializers.ReadOnlyField()

    class Meta:
        model = Student
        fields = [
            'student_id',
            'user',
            'nok_first_name',
            'nok_last_name',
            'nok_email',
            'nok_phone',
            'nok_relationship',
            'nok_occupation',
            'total_fees',
            'payment_status',
            'driving_exam_date',
            'driving_pdl_date',
            'driving_pdl',
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        courses = validated_data.pop('courses', [])

        user = User.objects.create(**user_data)
        student = Student.objects.create(user=user, **validated_data)

        if courses:
            student.courses.set(courses)

        return student


class StudentModuleSerializer(serializers.ModelSerializer):
    module_title = serializers.CharField(source='module.title', read_only=True)
    module_order = serializers.IntegerField(source='module.order', read_only=True)
    course_name = serializers.CharField(source='module.course.name', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    instructor_name = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentModule
        fields = [
            'id',
            'student',
            'student_name',
            'student_id',
            'module',
            'module_title',
            'module_order',
            'course_name',
            'status',
            'comment',
            'date_graded',
            'instructor',
            'instructor_name',
        ]
        read_only_fields = ['id', 'student', 'module', 'date_graded']
    
    def get_instructor_name(self, obj):
        if obj.instructor:
            return obj.instructor.user.get_full_name()
        return None