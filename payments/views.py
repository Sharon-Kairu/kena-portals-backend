from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from students.models import Student
from decimal import Decimal, InvalidOperation

class RegisterPaymentView(APIView):
    def post(self, request):
        try:
            student_id = request.data.get('student_id')
            amount = request.data.get('amount')
            payment_method = request.data.get('payment_method')
            transaction_code = request.data.get('transaction_code')
            
            print(f"Received data: {request.data}")  # Debug log
            
            # Validate required fields
            if not student_id:
                return Response(
                    {"error": "Student ID is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not amount:
                return Response(
                    {"error": "Amount is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not payment_method:
                return Response(
                    {"error": "Payment method is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate payment method
            valid_methods = ['mpesa', 'cash', 'bank']
            if payment_method not in valid_methods:
                return Response(
                    {"error": f"Invalid payment method. Must be one of: {', '.join(valid_methods)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Convert amount to Decimal
            try:
                amount = Decimal(str(amount))
                if amount <= 0:
                    return Response(
                        {"error": "Amount must be greater than 0"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except (InvalidOperation, ValueError) as e:
                return Response(
                    {"error": "Invalid amount format"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get student
            try:
                student = Student.objects.get(student_id=student_id)
            except Student.DoesNotExist:
                return Response(
                    {"error": f"Student with ID {student_id} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Create payment (receipt_number is auto-generated in save method)
            payment = Payment.objects.create(
                student=student,
                amount=amount,
                payment_method=payment_method,
                transaction_code=transaction_code if transaction_code else None
            )
            
            print(f"Payment created: {payment.receipt_number}")  # Debug log
            
            return Response({
                "message": "Payment registered successfully",
                "receipt_number": payment.receipt_number,
                "amount": str(payment.amount),
                "payment_method": payment.payment_method,
                "student": f"{student.user.first_name} {student.user.last_name}"
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            # Log the full error
            print(f"Error registering payment: {e}")
            import traceback
            traceback.print_exc()
            
            return Response(
                {"error": f"Server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class GetAllPaymentsView(APIView):
    def get(self, request):
        try:
            payments = Payment.objects.select_related(
                'student__user'
            ).order_by('-payment_date', '-id')
            
            data = []
            for payment in payments:
                data.append({
                    'id': payment.id,
                    'student': {
                        'student_id': payment.student.student_id,
                        'user': {
                            'first_name': payment.student.user.first_name,
                            'last_name': payment.student.user.last_name,
                        },
                        'total_fees': str(payment.student.total_fees) if payment.student.total_fees else '0'
                    },
                    'amount': str(payment.amount),
                    'payment_date': payment.payment_date.isoformat(),
                    'payment_method': payment.payment_method,
                    'transaction_code': payment.transaction_code,
                    'receipt_number': payment.receipt_number
                })
            
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Error fetching payments: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetEachStudentPaymentsView(APIView):
    def get(self,request,student_id):
        try:
            student=Student.objects.get(student_id=student_id)
            payments=Payment.objects.filter(student)
            data=[]
            for payment in payments:
                data.append({
                    'id': payment.id,
                    'student': {
                        'student_id': payment.student.student_id,
                        'user': {
                            'first_name': payment.student.user.first_name,
                            'last_name': payment.student.user.last_name,
                        },
                        'total_fees': str(payment.student.total_fees) if payment.student.total_fees else '0'
                    },
                    'amount': str(payment.amount),
                    'payment_date': payment.payment_date.isoformat(),
                    'payment_method': payment.payment_method,
                    'transaction_code': payment.transaction_code,
                    'receipt_number': payment.receipt_number
                })
            return Response(data, status=status.HTTP_200_OK)
                
        except:
            print(f"Error fetching payments: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

