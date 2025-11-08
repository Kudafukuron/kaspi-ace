from rest_framework import generics, permissions
from .models import Product
from .serializers import ProductSerializer
from users.permissions import IsOwnerOrManager, IsOwnerManagerOrReadOnly
from suppliers.models import LinkRequest

class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Consumer can only see accepted request supplier products.
        if user.role == "consumer":
            accepted_suppliers = LinkRequest.objects.filter(
                consumer=user,
                status="accepted"
            ).values_list("supplier_id", flat=True)
            return Product.objects.filter(supplier_id__in=accepted_suppliers, is_available=True)

        # owner's products.
        elif user.role == "owner":
            return Product.objects.filter(supplier__owner=user)

        # Manager, sales products.
        elif user.role in ["manager", "sales"]:
            return Product.objects.filter(supplier=user.supplier)

        # none
        return Product.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if hasattr(user, "supplier") and user.supplier:
            supplier = user.supplier  # For managers and sales
        elif hasattr(user, "owned_suppliers"):
            supplier = user.owned_suppliers.first()  # for owners
        else:
            raise ValueError("The user doesn't have this supplier")

        if not supplier:
            raise ValueError("Supplier hasn't found.")

        serializer.save(supplier=supplier)



class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/products/<id>/     — get    the product
    PATCH /api/products/<id>/   — update the product
    DELETE /api/products/<id>/  — delete the product
    """
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerManagerOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if getattr(user, "role", None) == "owner":
            return Product.objects.filter(supplier__owner=user)

        elif getattr(user, "role", None) in ["manager", "sales"]:
            return Product.objects.filter(supplier=user.supplier)

        elif getattr(user, "role", None) == "consumer":
            accepted_supplier_ids = LinkRequest.objects.filter(
                consumer=user, status="accepted"
            ).values_list("supplier_id", flat=True)
            return Product.objects.filter(supplier_id__in=accepted_supplier_ids)

        return Product.objects.none()