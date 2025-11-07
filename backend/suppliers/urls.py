from rest_framework import routers
from .views import SupplierViewSet, DeactivateSupplierView, ActivateSupplierView, SupplierEmployeesView, EmployeeManageView
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'suppliers', SupplierViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:supplier_id>/deactivate/', DeactivateSupplierView.as_view(), name='deactivate_supplier'),
    path('<int:supplier_id>/activate/', ActivateSupplierView.as_view(), name='activate_supplier'),
    path('<int:supplier_id>/employees/', SupplierEmployeesView.as_view(), name='supplier_employees'),
    path('<int:supplier_id>/employees/<int:employee_id>/toggle/', EmployeeManageView.as_view(), name='toggle_employee'),
    path('<int:supplier_id>/employees/<int:employee_id>/delete/', EmployeeManageView.as_view(), name='delete_employee'),
]
