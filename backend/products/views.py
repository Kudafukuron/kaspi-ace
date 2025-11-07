from rest_framework import generics, permissions
from .models import Product
from .serializers import ProductSerializer
from users.permissions import IsOwnerOrManager

class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrManager]

    # items for specific supplier.
    def get_queryset(self):
        return Product.objects.filter(supplier__owner=self.request.user)

    def perform_create(self, serializer):
        supplier = self.request.user.supplier or self.request.user.suppliers_owned.first()
        serializer.save(supplier=supplier)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrManager]

    def get_queryset(self):
        return Product.objects.filter(supplier__owner=self.request.user)
