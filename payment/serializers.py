from rest_framework import serializers
from listing.models import PropertyOffer
from .models import PaymentIntent, Transaction, Payment


class PaymentIntentSerializer(serializers.ModelSerializer):
    offer = serializers.PrimaryKeyRelatedField(
        queryset=PropertyOffer.objects.filter(status='accepted'),
        write_only=True,
    )
    property_slug = serializers.CharField(source='property_paid_for.slug', read_only=True)
    offer_id = serializers.IntegerField(source='offer.id', read_only=True)

    class Meta:
        model = PaymentIntent
        fields = [
            'id', 'offer', 'offer_id', 'property_slug', 'amount', 'currency', 'payment_mode',
            'phone_number', 'status', 'merchant_request_id', 'checkout_request_id',
            'provider_reference', 'failure_reason', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'offer_id', 'property_slug', 'amount', 'currency', 'payment_mode', 'status', 'merchant_request_id',
            'checkout_request_id', 'provider_reference', 'failure_reason',
            'created_at', 'updated_at',
        ]

    def validate_phone_number(self, value):
        normalized = ''.join(value.split())
        if normalized.startswith('+'):
            normalized = normalized[1:]
        if not normalized.isdigit() or not 9 <= len(normalized) <= 15:
            raise serializers.ValidationError('Enter a valid mobile phone number.')
        return value

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
        read_only_fields = ['id', 'date_paid', 'payment', 'payment_details']

    def get_payment_details(self, obj):
        return PaymentSummarySerializer(obj.payment).data


class PaymentSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = ['id', 'price', 'user', 'payment_mode', 'description', 'added_at', 'updated_at', 'transactions']
        read_only_fields = ['id', 'user', 'added_at', 'updated_at', 'transactions']
