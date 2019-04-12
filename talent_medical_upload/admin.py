from django.contrib import admin
from . import models

@admin.register(models.TalentMedicalUpload)
class TalentMedicalUploadAdmin(admin.ModelAdmin):
    list_display = (
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
    list_display_links = (
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
    list_per_page = 25
