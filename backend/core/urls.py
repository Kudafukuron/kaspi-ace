from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Users
    path('api/auth/', include('users.urls')),
    # Suppliers
    path('api/suppliers/', include('suppliers.urls')),
    # Products
    path('api/products/', include('products.urls')),
]
