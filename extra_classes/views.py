from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from .models import Request
from .serializers import RequestSerializer
from students.models import Student
from django.utils import timezone

class RegisterRequest(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        user = request.user

        # Get student object
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response(
                {"detail": "Student profile not found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Extract data
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=student, date_posted=timezone.now(), status='pending')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListRequests(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if  user.role == 'superadmin' or user.role=='admin':
            requests = Request.objects.all().order_by('-date_posted')
        else:
            try:
                student = Student.objects.get(user=user)
            except Student.DoesNotExist:
                return Response(
                    {"detail": "Student profile not found for this user."},
                    status=status.HTTP_404_NOT_FOUND
                )
            requests = Request.objects.filter(student=student).order_by('-date_posted')

        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateRequestStatus(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, request_id):
        try:
            extra_class_request = Request.objects.get(id=request_id)
        except Request.DoesNotExist:
            return Response(
                {"detail": "Request not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get('status')
        if new_status not in ['approved', 'denied']:
            return Response(
                {"detail": "Invalid status. Must be 'approved' or 'denied'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        extra_class_request.status = new_status
        extra_class_request.save()

        serializer = RequestSerializer(extra_class_request)
        return Response(serializer.data, status=status.HTTP_200_OK)
