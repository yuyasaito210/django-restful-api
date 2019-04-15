from authentication.models import User
from casting_request_talent.models import CastingRequestTalent
from invoice.models import Invoice
from invoice.serializers import InvoiceSerializer, InvoiceCreateSerializer
from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.core import serializers
from django.http import HttpResponse
import json


class InvoiceList(APIView):
    """
    Retrieve all invoices of client.
    """
    @swagger_auto_schema(responses={200: InvoiceSerializer(many=True)})
    def get(self, request, format=None):
        user = User.objects.get(pk=request.user.pk)
        invoices = Invoice.objects.all
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)

class InvoiceDetail(APIView):
    """
    Retrieve, update or delete a casting request of client.
    """
    def get_object(self, pk):
        try:
            return Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            raise Http404

    @swagger_auto_schema(responses={200: InvoiceSerializer(many=False)})
    def get(self, request, pk, format=None):
        invoice = self.get_object(pk)
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: InvoiceSerializer(many=False)})
    def put(self, request, pk, format=None):
        invoice = self.get_object(pk)
        serializer = InvoiceSerializer(invoice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: 'OK'})
    def delete(self, request, pk, format=None):
        invoice = self.get_object(pk)
        invoice.delete()

        return Response({'id': int(pk)}, status=status.HTTP_200_OK)


class InvoiceBulkCreate(APIView):
    """
    Create invoices for each casting_request_talent
    """
    # def get_object(self, user):
    #   try:
    #     user = User.objects.get(pk=user.pk)
    #     client = Client.objects.get(user=user.id)
    #     return client
    #   except Client.DoesNotExist:
    #     raise Http404

    @swagger_auto_schema(request_body=InvoiceCreateSerializer(many=True),
                         responses={200: InvoiceSerializer(many=True)})
    def post(self, request, format=None):
        # client = self.get_object(request.user)
        serializer = InvoiceCreateSerializer(data=request.data, many=True)

        if serializer.is_valid():
            new_crt_ids = []
            for invoice_data in serializer.validated_data:
                new_invoice = Invoice(**invoice_data)
                new_invoice.save()
                new_crt_ids.append(new_invoice.id)

            new_invoices = Invoice.objects.all().filter(id__in=new_crt_ids)
            new_serializer = InvoiceSerializer(new_invoices, many=True)
            return Response(new_serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
