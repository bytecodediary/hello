from .models import Payment, Transaction
from rest_framework import status, permissions, generics, response
from .serializers import PaymentSerializer, TransactionSerializer

class PaymentView(generics.GenericAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    # this is a sample implimentation and will impliment something better later
    def get_queryset(self, request):
        queryset = Payment.objects.all()
        queryset.user = request.user
        queryset.save()
        return queryset

class TransactionView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    # still learning the implmentation of the this view to include the payment gateway
    def Post(self):
        return response(status=status.HTTP_100_CONTINUE)