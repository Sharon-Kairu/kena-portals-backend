from rest_framework import serializers
from instructors.models import Instructor
from users.serializer import UserSerializer


class InstructorSerializer(serializers.ModelSerializer):
    user = UserSerializer() 

    class Meta:
        model = Instructor
        fields = ['user', 'category', 'national_id', 'instructor_id', 'date_of_birth',
                  'nok_first_name', 'nok_last_name', 'nok_email', 'nok_phone', 'nok_relationship', 'nok_occupation']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        instructor = Instructor.objects.create(user=user, **validated_data)
        return instructor
