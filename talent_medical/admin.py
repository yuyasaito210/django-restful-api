from django.contrib import admin
from . import models

@admin.register(models.TalentMedical)
class TalentMedicalAdmin(admin.ModelAdmin):
    list_display = (
    	'talent',
    	'condition_title',
    	'condition_value'
    )
    list_display_links = (
    	'talent',
    	'condition_title',
    	'condition_value'
    )
    list_per_page = 25
