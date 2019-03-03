from rest_framework import serializers
from talent_availability.models import TalentAvailability


class TalentAvailabilitySerializerWithoutTalentID(serializers.ModelSerializer):

    class Meta:
        model = TalentAvailability
        fields = ('id', 'start_date', 'end_date', 'updated_at')


class TalentAvailabilitySerializer(serializers.ModelSerializer):
    talent = serializers.SlugRelatedField(many=False, read_only=True, slug_field='id')

    class Meta:
        model = TalentAvailability
        fields = ('id', 'talent', 'start_date', 'end_date', 'updated_at')
