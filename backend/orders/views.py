from rest_framework import generics, permissions
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
