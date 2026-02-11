from django.urls import path,include
from .views import RegisterRequest, ListRequests, UpdateRequestStatus

urlpatterns = [
    path('register/',RegisterRequest.as_view(),name='Register Request' ),
    path('all_request/',ListRequests.as_view(), name='All Requests'),
    path('update_status/<int:request_id>/',UpdateRequestStatus.as_view(), name='Update Request Status'),
]
