from rest_framework import serializers
from position_sub_type.models import PositionSubType


class PositionSubTypeSerializer(serializers.ModelSerializer):
    position_type = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')

    class Meta:
        model = PositionSubType
        fields = (
            'id',
            'name',
            'abbreviated_key',
            'priority',
            'position_type',
            'select_option_title',
            'wizard_button_title',
            'video_audition_button_title',
            'agent_title',
        )
