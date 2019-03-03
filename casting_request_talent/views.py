from authentication.models import User
from client.models import Client
from casting_request.models import CastingRequest
from casting_request_talent.models import CastingRequestTalent
from casting_request_talent.serializers import CastingRequestTalentSerializer, CastingRequestTalentCreateSerializer
from talent_rating.models import TalentRating
from user_note.models import UserNoteManager
from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.core import serializers
from django.http import HttpResponse
import json


class CastingRequestTalentList(APIView):
    """
    Retrieve all casting requests of client.
    """
    @swagger_auto_schema(responses={200: CastingRequestTalentSerializer(many=True)})
    def get(self, request, format=None):
        user = User.objects.get(pk=request.user.pk)
        client = Client.objects.get(user=user)
        casting_requests = CastingRequest.objects.filter(client_id=client.id)
        casting_request_talents = CastingRequestTalent.objects.filter(
                casting_request_id__in=casting_requests.values_list('id')
        )
        serializer = CastingRequestTalentSerializer(casting_request_talents, many=True)
        return Response(serializer.data)


class CastingRequestTalentCompletedList(APIView):
    """
    Retrieve all completed casting requests of client.
    """
    @swagger_auto_schema(responses={200: CastingRequestTalentSerializer(many=True)})
    def get(self, request, format=None):
        user = User.objects.get(pk=request.user.pk)
        client = Client.objects.get(user=user)
        casting_requests = CastingRequest.objects.filter(client_id=client.id, status='Completed')
        casting_request_talents = CastingRequestTalent.objects.filter(
                casting_request_id__in=casting_requests.values_list('id')
        )
        unrated_casting_request_talents = []
        for crt in casting_request_talents:
            talent_rating_count = TalentRating.objects.filter(casting_request_talent=crt).count()
            if talent_rating_count == 0:
                unrated_casting_request_talents.append(crt)

        serializer = CastingRequestTalentSerializer(unrated_casting_request_talents, many=True)
        return Response(serializer.data)


class CastingRequestTalentDetail(APIView):
    """
    Retrieve, update or delete a casting request of client.
    """
    def get_object(self, pk):
        try:
            return CastingRequestTalent.objects.get(pk=pk)
        except CastingRequestTalent.DoesNotExist:
            raise Http404

    @swagger_auto_schema(responses={200: CastingRequestTalentSerializer(many=False)})
    def get(self, request, pk, format=None):
        casting_request_talent = self.get_object(pk)
        serializer = CastingRequestTalentSerializer(casting_request_talent)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: CastingRequestTalentSerializer(many=False)})
    def put(self, request, pk, format=None):
        casting_request_talent = self.get_object(pk)
        serializer = CastingRequestTalentSerializer(casting_request_talent, data=request.data)
        if serializer.is_valid():
            serializer.save()

            client_user = casting_request_talent.casting_request.client.user
            talent_user = casting_request_talent.talent.user
            UserNoteManager.casting_request_talent_logger(
                None, client_user, talent_user, 
                '{client} updated status of talent {talent} in casting reqeust.'.format(
                    client=client_user.first_name,
                    talent=talent_user.first_name
                ),
                casting_request_talent
            )

            return Response(serializer.data)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: 'OK'})
    def delete(self, request, pk, format=None):
        casting_request_talent = self.get_object(pk)
        casting_request_talent.delete()

        client_user = casting_request_talent.casting_request.client.user
        talent_user = casting_request_talent.talent.user
        UserNoteManager.casting_request_talent_logger(
            None, client_user, talent_user, 
            '{client} removed talent {talent} from casting reqeust.'.format(
                client=client_user.first_name,
                talent=talent_user.first_name
            ),
            casting_request_talent
        )

        return Response({'id': int(pk)}, status=status.HTTP_200_OK)


class CastingRequestTalentBulkCreate(APIView):
    """
    Create casting requests for each talent
    """
    # authentication_classes = (authentication.TokenAuthentication, )
    # permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, user):
      try:
        user = User.objects.get(pk=user.pk)
        client = Client.objects.get(user=user.id)
        return client
      except Client.DoesNotExist:
        raise Http404

    @swagger_auto_schema(request_body=CastingRequestTalentCreateSerializer(many=True),
                         responses={200: CastingRequestTalentSerializer(many=True)})
    def post(self, request, format=None):
        client = self.get_object(request.user)
        serializer = CastingRequestTalentCreateSerializer(data=request.data, many=True)

        if serializer.is_valid():
            new_crt_ids = []
            for casting_request_talent_data in serializer.validated_data:
                new_casting_request_talent = CastingRequestTalent(**casting_request_talent_data)
                new_casting_request_talent.save()

                client_user = new_casting_request_talent.casting_request.client.user
                talent_user = new_casting_request_talent.talent.user
                UserNoteManager.casting_request_talent_logger(
                    None, client_user, talent_user, 
                    '{client} added talent {talent} into casting reqeust.'.format(
                        client=client_user.first_name,
                        talent=talent_user.first_name,
                        casting_request=new_casting_request_talent.casting_request.id
                    ),
                    new_casting_request_talent
                )
                
                new_crt_ids.append(new_casting_request_talent.id)

            new_casting_request_talents = CastingRequestTalent.objects.all().filter(id__in=new_crt_ids)
            new_serializer = CastingRequestTalentSerializer(new_casting_request_talents, many=True)
            return Response(new_serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
