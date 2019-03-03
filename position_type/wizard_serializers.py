from rest_framework import serializers
from position_type.models import PositionType
from position_sub_type.wizard_serializers import WizardPositionSubTypeSerializer


class WizardPositionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PositionType
        fields = (
            'id',
            'name',
            'abbreviated_key',
            'priority',
            'wizard_button_title',
            'select_option_title',
            'agent_title',
            'introduction_link'
        )
