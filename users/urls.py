from django.urls import path,include
from .views import LoginView, RefreshTokenView,MeView,RegisterView
from dj_rest_auth.jwt_auth import get_refresh_view

urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    path('me/',MeView.as_view(),name='me'),
    path('register/',RegisterView.as_view(),name='register'),
]
