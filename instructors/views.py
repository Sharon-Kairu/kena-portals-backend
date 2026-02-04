from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from users.models import User
from .serializers import InstructorSerializer
from .models import Instructor

class RegisterInstructorView(APIView):
    permission_classes = [IsAuthenticated]  # Only admins can register instructors
    
    def post(self, request):
        try:
            with transaction.atomic():
                # 1. Extract and validate user data
                user_data = request.data.get('user', {})
                
                if not user_data:
                    return Response({
                        "message": "Error registering instructor",
                        "errors": {"user": ["User data is required"]}
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # 2. Create the user account
                try:
                    user = User.objects.create_user(
                        email=user_data.get('email'),
                        password=user_data.get('password'),
                        first_name=user_data.get('first_name', ''),
                        last_name=user_data.get('last_name', ''),
                        phone_number=user_data.get('phone_number', ''),
                        role=user_data.get('role', 'instructor')
                    )
                except Exception as e:
                    return Response({
                        "message": "Error creating user account",
                        "errors": {"user": [str(e)]}
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # 3. Prepare instructor data
                instructor_data = {
                    'user': user.id,
                    'course_name': request.data.get('course'),  # Use course_name field
                    'category_name': request.data.get('category', ''),  # Use category_name field
                    'national_id': request.data.get('national_id'),
                    'instructor_id': request.data.get('instructor_id'),
                    'date_of_birth': request.data.get('date_of_birth'),
                    'nok_first_name': request.data.get('nok_first_name'),
                    'nok_last_name': request.data.get('nok_last_name'),
                    'nok_email': request.data.get('nok_email', ''),
                    'nok_phone': request.data.get('nok_phone'),
                    'nok_relationship': request.data.get('nok_relationship'),
                    'nok_occupation': request.data.get('nok_occupation', ''),
                }
                
                # 4. Create the instructor
                serializer = InstructorSerializer(data=instructor_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        "message": "Instructor registered successfully",
                        "data": serializer.data
                    }, status=status.HTTP_201_CREATED)
                else:
                    # If instructor creation fails, the transaction will rollback
                    # and the user won't be created either
                    return Response({
                        "message": "Error registering instructor",
                        "errors": serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
        except Exception as e:
            return Response({
                "message": "Error registering instructor",
                "errors": {"detail": [str(e)]}
            }, status=status.HTTP_400_BAD_REQUEST)
        
class GetInstructors(APIView):
    def get(self,request):
        instructors=Instructor.objects.all()
        ser=InstructorSerializer
        if ser.is_valid():
            ser.save
        return instructors