from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .permissions import IsOwner, IsOwnerOrManager
from .models import User

User = get_user_model()

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": getattr(user, "role", None)
        })

class ConsumerRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['role'] = 'consumer' 
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Consumer registered successfully, suii",
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateManagerView(APIView):
    # Manager account creation endpoint, accessible only for owners
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request):
        data = request.data.copy()
        data["role"] = "manager" 
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Manager created successfully",
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateSalesView(APIView):
    # Endpoint for creating a salesman account
    permission_classes = [IsAuthenticated, IsOwnerOrManager]

    def post(self, request):
        data = request.data.copy()
        data["role"] = "sales"
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Sales account created successfully, suii",
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeactivateUserView(APIView):
    # Owner -> delete managers, salesmans.
    # Manager -> delete salesmans.
    permission_classes = [IsAuthenticated, IsOwnerOrManager]

    def patch(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Manager wants to delete higher than salesman 
        if request.user.role == 'manager' and target_user.role != 'sales':
            return Response({"detail": "Managers can only deactivate sales."}, status=status.HTTP_403_FORBIDDEN)

        target_user.is_active = False
        target_user.save()

        return Response({
            "message": f"User '{target_user.username}' has been deactivated.",
            "user": {
                "id": target_user.id,
                "username": target_user.username,
                "role": target_user.role,
                "is_active": target_user.is_active
            }
        }, status=status.HTTP_200_OK)
