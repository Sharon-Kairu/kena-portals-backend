from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated
from enrollments.models import Enrollment
from enrollments.serializers import EnrollmentSerializer

class AllStudentsView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class IndividualStudentView(APIView):
    def get(self, request, student_id):
        try:
            student = Student.objects.select_related('user').get(student_id=student_id)
            student_serializer = StudentSerializer(student)
            
            # Get enrollment data
            try:
                enrollment = Enrollment.objects.prefetch_related(
                    'standalone_courses',
                    'subscription_courses',
                    'subscription_plan'
                ).get(student=student)
                enrollment_serializer = EnrollmentSerializer(enrollment)
                enrollment_data = enrollment_serializer.data
            except Enrollment.DoesNotExist:
                enrollment_data = None
            
            return Response({
                'student': student_serializer.data,
                'enrollment': enrollment_data
            }, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def patch(self, request, student_id):
        """Update student details"""
        try:
            student = Student.objects.get(student_id=student_id)
            
            # Update student fields
            for field in ['nok_first_name', 'nok_last_name', 'nok_email', 'nok_phone', 
                         'nok_relationship', 'nok_occupation', 'total_fees', 'payment_status',
                         'driving_exam_date', 'driving_pdl_date', 'driving_pdl']:
                if field in request.data:
                    setattr(student, field, request.data[field])
            
            # Update user fields if provided
            if 'user' in request.data:
                user = student.user
                user_data = request.data['user']
                for field in ['first_name', 'last_name', 'email', 'phone_number']:
                    if field in user_data:
                        setattr(user, field, user_data[field])
                user.save()
            
            student.save()
            
            serializer = StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )   

class MeStudentView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        user = request.user


        try:
         student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response(
            {"detail": "Student profile not found for this user"},
            status=status.HTTP_404_NOT_FOUND
        )


        return Response({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role,


        "student_id": student.student_id,
        "total_fees": str(student.total_fees),
        "payment_status": student.payment_status,
        "exam_date": student.driving_exam_date,
        "pdl_date": student.driving_pdl_date,
        "pdl": student.driving_pdl,


        "nok_first_name": student.nok_first_name,
        "nok_last_name": student.nok_last_name,
        "nok_phone": student.nok_phone,
        })

