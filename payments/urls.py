from django.urls import path,include
from .views import RegisterPaymentView,GetAllPaymentsView,GetEachStudentPaymentsView


urlpatterns = [
    path('register/', RegisterPaymentView.as_view(), name='register-payment'),
    path('all/', GetAllPaymentsView.as_view(), name='all-payments'),
    
]
