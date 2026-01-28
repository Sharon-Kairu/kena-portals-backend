from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import InstructorSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class RegisterInstructorView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = InstructorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Instructor registered successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Error registering instructor",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
