from .models import Payment, Transaction
from rest_framework import permissions, generics
from .serializers import PaymentSerializer, TransactionSerializer


class PaymentView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Payment.objects.filter(user=self.request.user)
            .select_related("user", "order", "property_paid_for")
            .prefetch_related("transactions")
            .order_by("-added_at")
        )

class TransactionView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Transaction.objects.filter(payment__user=self.request.user)
            .select_related("payment", "payment__user", "payment__property_paid_for")
            .order_by("-date_paid")
        )
