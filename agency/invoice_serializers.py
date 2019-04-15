from rest_framework import serializers


class InvoiceSearchSerializer(serializers.Serializer):
    casting_reuqest_talent_id = serializers.IntegerField(required=False)