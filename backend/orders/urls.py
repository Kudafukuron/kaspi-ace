from django.urls import path
from .views import OrderCreateView, OrderUpdateStatusView, OrderListView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/status/', OrderUpdateStatusView.as_view(), name='order-update-status'),
]
