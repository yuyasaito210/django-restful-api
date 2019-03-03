from rest_framework import serializers
from .models import TalentResume

class TalentResumeSerializer(serializers.ModelSerializer):
  # talent = serializers.SlugRelatedField(many=False, read_only=True, slug_field='id')

  class Meta:
    model = TalentResume
    fields = (
        'id', 
        'talent',
        'approved',
        'approved_date',
        'approved_by',
        'name', 
        'path', 
        'url',
        'size', 
        'file_type', 
        'timestamp', 
        'updated', 
        'uploaded', 
        'active', 
        'preview_path'
      )