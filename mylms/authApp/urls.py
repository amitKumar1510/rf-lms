from django.urls import path
from .views import (
    UserRegistrationView,
    AdminUserRegistrationView,
    UserListView,
    CustomTokenObtainPairView,DeleteUserView, UpdateUserRoleByRole,DeactivateAndActivteUserView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # JWT Authentication
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User Registration
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    # path('admin/register/', AdminUserRegistrationView.as_view(), name='admin-register'),

    # User Management (Admin only)
    path('users/', UserListView.as_view(), name='user-list'),

    # path('users/role/<str:role>/', UserByRoleListView.as_view(), name='user-by-role'),

    path('users/<str:Uid>/update-role/', UpdateUserRoleByRole.as_view(), name='update-user-role-by-role'),

    path('users/delete/', DeleteUserView.as_view(), name='delete-own-account'),
    path('users/delete/<str:Uid>/', DeleteUserView.as_view(), name='delete-user-by-uid'),
    path('users/deactivate/<str:Uid>/', DeactivateAndActivteUserView.as_view(), name='deactivate-user'),

]
