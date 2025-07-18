from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer, AdminUserSerializer
from .permission import IsAdmin
from .models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .permission import is_role_change_allowed

# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Common.EmailServices import MailService


ALLOWED_ROLES = [
    CustomUser.ADMIN,
    CustomUser.PRINCIPAL,
    CustomUser.TEACHER,
    CustomUser.STUDENT,
    CustomUser.PARENT,
]

# class UserRegistrationView(APIView):
#     """
#     Register a new user (default role: student).
#     """
#     permission_classes = [IsAuthenticated, IsAdmin]  # Only admins can register users
#     def post(self, request):
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             user =  serializer.save()
#             # token_serializer = CustomTokenObtainPairSerializer(data={
#             #     "email": user.email,
#             #     "password": request.data["password"]
#             # })
#             # token_serializer.is_valid(raise_exception=True)
#             # token_data = token_serializer.validated_data
#             return Response({
#                 # "user": serializer.data,
#                 # "token": token_data
#                 "message": "User registered successfully",
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminUserRegistrationView(APIView):
    """
    Allows admin to register a user with any role.
    Only admins can access this view.
    """
    # permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        role = request.data.get('role')
        email = request.data.get('email')
        password = request.data.get('password', "your DOB")
        first_name = request.data.get('first_name', 'User')
        if role not in ALLOWED_ROLES:
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AdminUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Send email with credentials
            MailService.send_Credentials(email, password)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    """
    List all users (admin-only access).
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class DeleteUserView(APIView):
    """
    Allows admin to deletes the data of user, princile, teachers etc. deletion using logic.
    """
    permission_classes = [IsAuthenticated,IsAdmin]

    def delete(self, request, Uid=None):
        try:
            if Uid:
                target_user = CustomUser.objects.get(Uid=Uid)
            else:
                target_user = request.user

            current_user = request.user

            if target_user == current_user:
                target_user.delete()
                return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

            if current_user.role == 'admin' or is_role_change_allowed(current_user, target_user.role):
                target_user.delete()
                return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

            return Response({'error': 'You are not authorized to delete this user.'}, status=status.HTTP_403_FORBIDDEN)

        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class UpdateUserRoleByRole(APIView):
    """
    Allows admin to update roles based on hierarchy:
    - Admin: can assign principal, teacher, parent
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, Uid):
        try:
            user = CustomUser.objects.get(Uid=Uid)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        new_role = request.data.get('role')
        if not new_role:
            return Response({'error': 'Role not provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Only allow if user has permission to assign this role
        if not is_role_change_allowed(request.user, new_role):
            return Response({'error': 'Not authorized to assign this role'}, status=status.HTTP_403_FORBIDDEN)

        user.role = new_role
        user.save()
        return Response({'message': f'User role updated to {new_role}'}, status=status.HTTP_200_OK)  
    

class DeactivateAndActivteUserView(APIView):
    """
    Toggles the `is_active` status of a user based on role hierarchy.
    - If user is active → deactivate
    - If user is inactive → activate
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, Uid):
        try:
            target_user = CustomUser.objects.get(Uid=Uid)
            current_user = request.user


            if target_user == current_user:
                target_user.is_active = not target_user.is_active
                target_user.save()
                status_msg = 'deactivated' if not target_user.is_active else 'activated'
                return Response({'message': f'Your account has been {status_msg}.'}, status=status.HTTP_200_OK)


            if current_user.role == 'admin' or is_role_change_allowed(current_user, target_user.role):
                target_user.is_active = not target_user.is_active
                target_user.save()
                status_msg = 'deactivated' if not target_user.is_active else 'activated'
                return Response({'message': f'User has been {status_msg}.'}, status=status.HTTP_200_OK)

            return Response({'error': 'You are not authorized to toggle this user\'s active status.'}, status=status.HTTP_403_FORBIDDEN)

        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
