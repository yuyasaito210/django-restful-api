from rest_framework import serializers
from .models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Invoice
        fields = (
            'id',
            'casting_request_talent',
            'inv_date',
            'inv_nbr',
            'inv_amt',
            'amt_paid',
            'date_paid',
            'balance',
            'created',
            'updated'
        )


class InvoiceCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = (
            'id',
            'inv_date',
            'inv_nbr',
            'inv_amt',
            'amt_paid',
            'date_paid',
            'balance',
        )

    def create(self, validated_data):
        return Invoice.objects.create(**validated_data)

