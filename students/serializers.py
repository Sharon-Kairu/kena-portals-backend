from rest_framework import serializers
from .models import Student
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