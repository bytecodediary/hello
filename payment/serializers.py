from rest_framework import serializers
from .models import Transaction, Payment


class PaymentSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'price', 'payment_mode', 'description', 'added_at']


class TransactionSerializer(serializers.ModelSerializer):
    payment_details = serializers.SerializerMethodField()
    payment = serializers.PrimaryKeyRelatedField(queryset=Payment.objects.all())

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'date_paid', 'transaction_desc', 'status', 'transaction_type', 'payment', 'payment_details']
        read_only_fields = ['id', 'date_paid']

    def get_payment_details(self, obj):
        return PaymentSummarySerializer(obj.payment).data


class PaymentSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = ['id', 'price', 'user', 'payment_mode', 'description', 'added_at', 'updated_at', 'transactions']
        read_only_fields = ['id', 'user', 'added_at', 'updated_at', 'transactions']