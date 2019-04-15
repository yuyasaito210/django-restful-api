from django.contrib import admin
from . import models
from rest_framework.authtoken.admin import TokenAdmin


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'casting_request_talent_display',
        'inv_date',
        'inv_nbr',
        'inv_amt',
        'amt_paid',
        'date_paid',
        'balance',
        'created',
        'updated'
    )
    list_display_links = (
        'id',
        'casting_request_talent_display',
        'inv_date',
        'inv_nbr',
        'inv_amt',
        'amt_paid',
        'date_paid',
        'balance',
        'created',
        'updated'
    )
    list_per_page = 25

    def casting_request_talent_display(self, obj):
        return obj.casting_request_request.name

    casting_request_talent_display.short_description = 'Casting Request Talent'