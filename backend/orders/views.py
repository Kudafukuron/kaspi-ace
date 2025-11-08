from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from products.models import Product

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.request.data.get('product')
        quantity = int(self.request.data.get('quantity', 1))

        product = Product.objects.get(id=product_id)
        total_price = product.price * quantity

        serializer.save(consumer=self.request.user, total_price=total_price)

class OrderUpdateStatusView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()
        user = request.user

        # Only sales, manager, owner can change the status of the order.
        if user.role not in ['manager', 'sales', 'owner']:
            return Response({"detail": "You don't have permission to change status."}, status=403)

        status = request.data.get("status")
        allowed_statuses = ["confirmed", "shipped", "delivered", "cancelled"]

        if status not in allowed_statuses:
            return Response({"detail": "Invalid status value."}, status=400)

        order.status = status
        order.save()
        return Response({
            "message": f"Order #{order.id} status updated to '{status}'.",
            "order": OrderSerializer(order).data
        })
    
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'consumer':
            return Order.objects.filter(consumer=user)
        elif user.role in ['manager', 'sales', 'owner']:
            return Order.objects.filter(product__supplier__owner=user)
        return Order.objects.none()
