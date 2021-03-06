from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from talent_position_type.models import TalentPositionType
from talent_position_type.serializers import TalentPositionTypeSerializer
from .serializers import TalentPositionTypeSerializer


class TalentPositionTypeViewSet(viewsets.ModelViewSet):
    queryset = TalentPositionType.objects.all()
    serializer_class = TalentPositionTypeSerializer
    # permission_classes = (IsAuthenticated,)


class TalentPositionTypeList(APIView):
    """
    List all talent_position_type.
    """
    def get(self, request, format=None):
        talent_position_type = TalentPositionType.objects.all()
        serializer = TalentPositionTypeSerializer(talent_position_type, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TalentPositionTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class TalentPositionTypeDetail(APIView):
    """
    Retrieve a talent_position_type_item instance.
    """
    def get_object(self, pk):
        try:
            return TalentPositionType.objects.get(pk=pk)
        except TalentPositionType.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        talent_position_type_item = self.get_object(pk)
        serializer = TalentPositionTypeSerializer(talent_position_type_item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        talent_position_type_item = self.get_object(pk)
        serializer = TalentPositionTypeSerializer(talent_position_type_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        talent_position_type_item = self.get_object(pk)
        talent_position_type_item.delete()
        return Response({'id': int(pk)}, status=status.HTTP_200_OK)
