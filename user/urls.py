from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('user_registration/', views.user_registration, name='register_user'),
    path('user_login/', views.user_login, name='login_user'),
    path('user_logout/', views.user_logout, name='logout_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
