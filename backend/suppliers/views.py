from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Supplier
from .serializers import SupplierSerializer
from users.permissions import IsOwnerOrManager
import traceback
from users.models import User

from rest_framework import viewsets, permissions
from .models import Supplier

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

class DeactivateSupplierView(APIView):
    # Manager or owner can deactivate the supplier account
    permission_classes = [IsAuthenticated, IsOwnerOrManager]

    def patch(self, request, supplier_id):
        try:
            supplier = Supplier.objects.get(id=supplier_id)
            supplier.is_active = False
            supplier.save()
            return Response({
                "message": f"Supplier '{supplier.name}' has been deactivated.",
                "supplier": SupplierSerializer(supplier).data
            }, status=status.HTTP_200_OK)
        except Supplier.DoesNotExist:
            return Response({"detail": "Supplier not found."}, status=status.HTTP_404_NOT_FOUND)
        
class ActivateSupplierView(APIView):
    # Activate the account, managers and owners only.
    permission_classes = [IsAuthenticated, IsOwnerOrManager]

    def patch(self, request, supplier_id):
        try:
            supplier = Supplier.objects.get(id=supplier_id)
        except Supplier.DoesNotExist:
            return Response({"detail": "Supplier not found."}, status=status.HTTP_404_NOT_FOUND)

        supplier.is_active = True
        supplier.save()

        return Response({
            "message": f"Supplier '{supplier.name}' has been activated.",
            "supplier": SupplierSerializer(supplier).data
        }, status=status.HTTP_200_OK)
    
# Owner lists all employees from the supplier company.
class SupplierEmployeesView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrManager]

    def get(self, request, supplier_id):
        try:
            supplier = Supplier.objects.get(id=supplier_id)
        
            # filter to supplier.
            employees = User.objects.filter(supplier=supplier).values(
                "id", "username", "email", "role", "is_active"
            )

            return Response({
                "supplier": supplier.name,
                "employees": list(employees)
            })
        
        # bruh, 500 errors are just solved by adding model views.
        except Supplier.DoesNotExist:
            return Response({"detail": "Supplier not found."}, status=404)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)
        
class EmployeeManageView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrManager]

    def patch(self, request, supplier_id, employee_id):
        try:
            supplier = Supplier.objects.get(id=supplier_id)
            employee = User.objects.get(id=employee_id, supplier=supplier)

            # Manager case, not enough rights.
            if request.user.role == 'manager' and employee.role in ['owner', 'manager']:
                return Response(
                    {"detail": "Managers cannot modify other managers or owners."},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Status update.
            employee.is_active = not employee.is_active
            employee.save()

            status_str = "activated" if employee.is_active else "deactivated"

            return Response({
                "message": f"Employee '{employee.username}' has been {status_str}.",
                "employee": {
                    "id": employee.id,
                    "username": employee.username,
                    "role": employee.role,
                    "is_active": employee.is_active
                }
            })

        except Supplier.DoesNotExist:
            return Response({"detail": "Supplier not found."}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, supplier_id, employee_id):
        # Delete the employee, DANGEROUS PLACE
        try:
            supplier = Supplier.objects.get(id=supplier_id)
            employee = User.objects.get(id=employee_id, supplier=supplier)

            # If manager tries to delete (guy wants too much power)
            if request.user.role == 'manager' and employee.role in ['owner', 'manager']:
                return Response(
                    {"detail": "Managers can only delete sales employees."},
                    status=status.HTTP_403_FORBIDDEN
                )

            username = employee.username
            employee.delete()

            return Response({
                "message": f"Employee '{username}' has been deleted successfully."
            }, status=status.HTTP_200_OK)

        except Supplier.DoesNotExist:
            return Response({"detail": "Supplier not found."}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
