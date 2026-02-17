# instructors/serializers.py
from rest_framework import serializers
from .models import Instructor
from courses.models import Course, CourseCategory
from users.serializer import UserSerializer


class InstructorListSerializer(serializers.ModelSerializer):
    """Serializer for listing instructors with basic information"""
    full_name = serializers.SerializerMethodField()
    course = serializers.CharField(source="course.name", read_only=True)
    category = serializers.CharField(source="category.name", read_only=True, allow_null=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)
    is_active=serializers.CharField(source="user.is_active", read_only=True)

    class Meta:
        model = Instructor
        fields = [
            "instructor_id",
            "full_name",
            "course",
            "category",
            "phone_number",
            "is_active",
            "user",
        ]

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


class InstructorDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed instructor information"""
    user = UserSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    course = serializers.CharField(source="course.name", read_only=True)
    category = serializers.CharField(source="category.name", read_only=True, allow_null=True)

    class Meta:
        model = Instructor
        fields = [
            "id",
            "instructor_id",
            "full_name",
            "user",
            "course",
            "category",
            "national_id",
            "license_number",
            "date_of_birth",
            "nok_first_name",
            "nok_last_name",
            "nok_email",
            "nok_phone",
            "nok_relationship",
            "nok_occupation",
        ]

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


class InstructorSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(write_only=True, required=False)
    category_name = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    full_name = serializers.SerializerMethodField()
    course = serializers.CharField(source="course.name", read_only=True)
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Instructor
        fields = [
            "id",
            "full_name",
            "course",
            "category",
            "user",
            "course_name",
            "category_name",
            "instructor_id",
            "license_number",
            "date_of_birth",
            "nok_first_name",
            "nok_last_name",
            "nok_email",
            "nok_phone",
            "nok_relationship",
            "nok_occupation",
        ]

        extra_kwargs = {
            "user": {"write_only": True},
        }

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def create(self, validated_data):
        course_name = validated_data.pop("course_name", None)
        category_name = validated_data.pop("category_name", None)

        # Get course by name
        if course_name:
            try:
                course = Course.objects.get(name=course_name)
                validated_data["course"] = course
            except Course.DoesNotExist:
                raise serializers.ValidationError({
                    "course_name": f'Course "{course_name}" does not exist'
                })

        # Get category by name (if provided and not empty)
        if category_name and category_name.strip():
            try:
                category = CourseCategory.objects.get(
                    course=validated_data["course"],
                    name=category_name
                )
                validated_data["category"] = category
            except CourseCategory.DoesNotExist:
                raise serializers.ValidationError({
                    "category_name": f'Category "{category_name}" does not exist for this course'
                })

        return super().create(validated_data)
