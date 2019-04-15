from rest_framework import serializers
from invoice.models import Invoice
from casting_request_talent.details_by_talent_serializers import CastingRequestTalentDetailByTalentSerializer


class InvoiceDetailSerializer(serializers.ModelSerializer):
    casting_request_talent = CastingRequestTalentDetailByTalentSerializer(many=False)

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
