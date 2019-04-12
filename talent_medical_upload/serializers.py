from rest_framework import serializers
from .models import TalentMedicalUpload

class TalentMedicalUploadSerializer(serializers.ModelSerializer):

  class Meta:
    model = TalentMedicalUpload
    fields = (
        'id',
        'talent', 
        'name', 
        'path', 
        'preview_path', 
        'url', 
        'size',
        'file_type',
        'timestamp',
        'updated', 
        'uploaded',
        'active'
      )