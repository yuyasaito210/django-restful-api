from authentication.models import User
from invoice.models import Invoice
from invoice.details_serializers import InvoiceDetailSerializer
from agency.invoice_serializers import InvoiceSearchSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class InvoiceSearch(APIView):
    """
    Retrieve all invoices of talent.
    """
    @swagger_auto_schema(request_body=InvoiceSearchSerializer, responses={200: InvoiceDetailSerializer(many=True)})
    def post(self, request, format=None):
        user = User.objects.get(pk=request.user.pk)
        if 'casting_request_talent_id' in request.data:
            invoices = Invoice.objects.filter(casting_request_talent_id=request.data['casting_request_talent_id'])
        else :
            invoices = Invoice.objects.all()
        serializer = InvoiceDetailSerializer(invoices, many=True)
        return Response(serializer.data)
