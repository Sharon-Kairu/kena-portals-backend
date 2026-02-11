# instructors/serializers.py
from rest_framework import serializers
from .models import Instructor
from courses.models import Course, CourseCategory

class InstructorSerializer(serializers.ModelSerializer):
    # WRITE-ONLY (for create)
    course_name = serializers.CharField(write_only=True, required=False)
    category_name = serializers.CharField(write_only=True, required=False, allow_blank=True)

    # READ-ONLY (for frontend)
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

            # keep these for create/update
            "user",
            "course_name",
            "category_name",

            # extra fields (still available if needed)
            "national_id",
            "instructor_id",
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

        # Get category by name (if provided)
        if category_name:
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
