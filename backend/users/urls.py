from django.urls import path
from .views import ConsumerRegisterView, MeView, CreateManagerView, CreateSalesView, DeactivateUserView, GetSalesmanForSupplier, MySuppliersView, SupplierConsumersView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('register/consumer/', ConsumerRegisterView.as_view(), name='register_consumer'),
    path('create-manager/', CreateManagerView.as_view(), name='create_manager'),
    path("create-sales/", CreateSalesView.as_view()),
    path('<int:user_id>/deactivate/', DeactivateUserView.as_view(), name='deactivate_user'),
    path("my-suppliers/", MySuppliersView.as_view()),
    path("salesman/<int:supplier_id>/", GetSalesmanForSupplier.as_view()),
    path("supplier/consumers/", SupplierConsumersView.as_view()),
]
