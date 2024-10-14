from rest_framework import serializers
from .models import Transaction, Payment

class TransactionSerializer(serializers.ModelSerializer):
    payment_details = serializers.SerializerMethodField()
    payment = serializers.PrimaryKeyRelatedField(read_only=True, source='payment.id')

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'date_paid', 'transaction_desc', 'payment_details', 'payment']

    def get_payment_details(self, obj):
        return PaymentSerializer(obj.payment).data

class PaymentSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, source='transactions', read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = ['id', 'price', 'user', 'transaction_type', 'updated_at', 'description', 'added_at', 'transactions']