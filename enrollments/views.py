from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from students.models import Student
from enrollments.models import Enrollment
from courses.models import SubscriptionPlan, Course
from instructors.models import Instructor
from students.utils import assign_modules_to_student

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_student(request):
    try:
        with transaction.atomic():
            # 1. Validate ALL data first before creating any records
            user_data = request.data.get('user', {})
            
            # Check required user fields
            required_user_fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'id_number']
            missing_user_fields = [field for field in required_user_fields if not user_data.get(field)]
            if missing_user_fields:
                return Response({
                    'message': 'Missing required student information',
                    'errors': {'user': [f"Required fields missing: {', '.join(missing_user_fields)}"]}
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check required student fields
            required_student_fields = ['nok_first_name', 'nok_last_name', 'nok_phone', 'nok_relationship', 'total_fees']
            missing_student_fields = [field for field in required_student_fields if not request.data.get(field)]
            if missing_student_fields:
                return Response({
                    'message': 'Missing required next of kin or fee information',
                    'errors': {'student': [f"Required fields missing: {', '.join(missing_student_fields)}"]}
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate courses and enrollment mode
            subscription_plan_id = request.data.get('subscription_plan')
            courses_ids = request.data.get('courses', [])
            
            if not subscription_plan_id and not courses_ids:
                return Response({
                    'message': 'Please select either a subscription plan or standalone courses',
                    'errors': {'courses': ['No courses or subscription plan selected']}
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 2. Create User only after all validation passes
            user = User.objects.create_user(
                role='student',
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                phone_number=user_data.get('phone'),
                id_number=user_data.get('id_number'),
            )
            
            # 2. Create Student
            student = Student.objects.create(
                user=user,    
                nok_first_name=request.data.get('nok_first_name'),
                nok_last_name=request.data.get('nok_last_name'),
                nok_email=request.data.get('nok_email'),
                nok_phone=request.data.get('nok_phone'),
                nok_relationship=request.data.get('nok_relationship'),
                nok_occupation=request.data.get('nok_occupation'),
                total_fees=request.data.get('total_fees', 0)
            )
            
            # 3. Determine mode based on subscription_plan ID
            subscription_plan_id = request.data.get('subscription_plan')
            courses_ids = request.data.get('courses', [])
            
            # Map subscription plan IDs: 1=bronze, 2=gold, 3=platinum
            if subscription_plan_id:
                mode = 'subscription'
                subscription_plan = SubscriptionPlan.objects.get(id=subscription_plan_id)
            else:
                mode = 'standalone'
                subscription_plan = None
            
            # 4. Create Enrollment (SAVE FIRST!)
            enrollment = Enrollment.objects.create(
                student=student,
                mode=mode,
                subscription_plan=subscription_plan
            )
            
            # 5. Add courses to M2M fields
            # Course IDs: 5=computer, 6=AI, 7=driving
            if courses_ids:
                courses = Course.objects.filter(id__in=courses_ids)
                
                if mode == 'standalone':
                    enrollment.standalone_courses.set(courses)
                else:
                    enrollment.subscription_courses.set(courses)
                
                # Assign all modules from enrolled courses to the student
                assign_modules_to_student(student, courses)
            
            # 6. Add instructors from instructor_assignments
            instructor_assignments = request.data.get('instructor_assignments', [])
            if instructor_assignments:
                instructor_ids = [assignment['instructor_id'] for assignment in instructor_assignments]
                instructors = Instructor.objects.filter(id__in=instructor_ids)
                enrollment.instructors.set(instructors)
            
            return Response({
                'message': 'Student enrolled successfully',
                'student_id': student.id,
                'enrollment_id': enrollment.id
            }, status=status.HTTP_201_CREATED)
            
    except SubscriptionPlan.DoesNotExist:
        return Response({
            'error': f'Subscription plan with ID {subscription_plan_id} does not exist'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Course.DoesNotExist:
        return Response({
            'error': 'One or more courses do not exist'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)