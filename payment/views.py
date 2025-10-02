from .models import Payment, Transaction
from rest_framework import permissions, generics
from rest_framework.exceptions import PermissionDenied
from .serializers import PaymentSerializer, TransactionSerializer


class PaymentView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Payment.objects.filter(user=self.request.user)
            .select_related("user", "order", "property_paid_for")
            .prefetch_related("transactions")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Transaction.objects.filter(payment__user=self.request.user)
            .select_related("payment", "payment__user", "payment__property_paid_for")
        )

    def perform_create(self, serializer):
        payment = serializer.validated_data.get("payment")
        if payment.user != self.request.user:
            raise PermissionDenied("You are not allowed to create transactions for this payment.")
        serializer.save()