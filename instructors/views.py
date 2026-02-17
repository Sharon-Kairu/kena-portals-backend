from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from users.models import User
from .serializers import InstructorSerializer, InstructorListSerializer, InstructorDetailSerializer
from .models import Instructor
from enrollments.models import Enrollment

class RegisterInstructorView(APIView):
    permission_classes = [IsAuthenticated]  # Only admins can register instructors
    
    def post(self, request):
        try:
            with transaction.atomic():
                # 1. Extract and validate ALL data first
                user_data = request.data.get('user', {})
                
                # Validate user data
                if not user_data:
                    return Response({
                        "message": "User data is required",
                        "errors": {"user": ["User data is required"]}
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Check required user fields
                required_user_fields = ['email', 'password', 'first_name', 'last_name', 'phone_number', 'national_id']
                missing_user_fields = [field for field in required_user_fields if not user_data.get(field)]
                if missing_user_fields:
                    return Response({
                        "message": "Missing required user fields",
                        "errors": {"user": [f"Required fields missing: {', '.join(missing_user_fields)}"]}
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Check required instructor fields
                required_instructor_fields = ['course', 'date_of_birth', 'nok_first_name', 'nok_last_name', 'nok_phone', 'nok_relationship']
                missing_instructor_fields = [field for field in required_instructor_fields if not request.data.get(field)]
                if missing_instructor_fields:
                    return Response({
                        "message": "Missing required instructor fields",
                        "errors": {"instructor": [f"Required fields missing: {', '.join(missing_instructor_fields)}"]}
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Validate course and category
                course_name = request.data.get('course')
                if not course_name:
                    return Response({
                        "message": "Course is required",
                        "errors": {"course": ["Please select a course"]}
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # If driving course, category is required
                if course_name == 'driving' and not request.data.get('category'):
                    return Response({
                        "message": "Category is required for driving instructors",
                        "errors": {"category": ["Please select a category (Theory or Practical)"]}
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # 2. Create the user account only after all validation passes
                try:
                    user = User.objects.create_user(
                        email=user_data.get('email'),
                        password=user_data.get('password'),
                        first_name=user_data.get('first_name'),
                        last_name=user_data.get('last_name'),
                        phone_number=user_data.get('phone_number'),
                        id_number=user_data.get('national_id'),
                        role='instructor'
                    )
                except Exception as e:
                    return Response({
                        "message": "Error creating user account",
                        "errors": {"user": [str(e)]}
                    }, status=status.HTTP_400_BAD_REQUEST)
            
                # 3. Prepare instructor data
                instructor_data = {
                    'user': user.id,
                    'course_name': course_name,
                    'category_name': request.data.get('category'),
                    'license_number': request.data.get('license_number', ''),
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
    """Get all instructors with basic information for listing"""
    def get(self, request):
        instructors = Instructor.objects.select_related('user', 'course', 'category').all()
        serializer = InstructorListSerializer(instructors, many=True) 
        return Response(serializer.data)


class IndividualInstructorView(APIView):
    """Get detailed information for a specific instructor"""
    def get(self, request, instructor_id):
        try:
            instructor = Instructor.objects.select_related('user', 'course', 'category').get(
                instructor_id=instructor_id
            )
            serializer = InstructorDetailSerializer(instructor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Instructor.DoesNotExist:
            return Response(
                {"error": "Instructor not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def patch(self, request, instructor_id):
        """Update instructor details"""
        try:
            instructor = Instructor.objects.get(instructor_id=instructor_id)
            
            # Update instructor fields
            for field in ['national_id', 'license_number', 'date_of_birth', 
                         'nok_first_name', 'nok_last_name', 'nok_email', 
                         'nok_phone', 'nok_relationship', 'nok_occupation']:
                if field in request.data:
                    setattr(instructor, field, request.data[field])
            
            # Update user fields if provided
            if 'user' in request.data:
                user = instructor.user
                user_data = request.data['user']
                for field in ['first_name', 'last_name', 'email', 'phone_number']:
                    if field in user_data:
                        setattr(user, field, user_data[field])
                user.save()
            
            instructor.save()
            
            serializer = InstructorDetailSerializer(instructor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Instructor.DoesNotExist:
            return Response(
                {"error": "Instructor not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
class InstructorStudents(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            instructor = Instructor.objects.get(user=request.user)
            enrollments = Enrollment.objects.filter(
                instructors=instructor
            ).select_related(
                'student',
                'subscription_plan'
            ).prefetch_related(
                'standalone_courses',
                'subscription_courses'
            )

            data = []

            for enrollment in enrollments:
                courses = []

                if enrollment.mode == 'standalone':
                    courses = enrollment.standalone_courses.all()
                elif enrollment.mode == 'subscription':
                    courses = enrollment.subscription_courses.all()

                data.append({
                    "student_id": enrollment.student.id,
                    "student_name": enrollment.student.user.get_full_name(),
                    "mode": enrollment.mode,
                    "subscription_plan": enrollment.subscription_plan.name
                    if enrollment.subscription_plan else None,
                    "courses": [
                        {
                            "id": course.id,
                            "name": course.name,
                        }
                        for course in courses
                    ]
                })

            return Response(data, status=status.HTTP_200_OK)

        except Instructor.DoesNotExist:
            return Response(
                {"detail": "Instructor profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

