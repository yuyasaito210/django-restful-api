from django.db import models
from casting_request_talent.models import CastingRequestTalent


class Invoice(models.Model):
    casting_request_talent = models.ForeignKey(
            CastingRequestTalent,
            related_name='casting_request_talent_invoices',
            on_delete=models.CASCADE
    )
    inv_date = models.DateTimeField(auto_now_add=True)
    inv_nbr = models.CharField(blank=False, default='', max_length=100)
    inv_amt = models.FloatField(blank=True, default=0.0)
    amt_paid = models.FloatField(blank=True, default=0.0)
    date_paid = models.DateTimeField(blank=True, null=True)
    balance = models.FloatField(blank=True, default=0.0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.inv_nbr

    class Meta:
        db_table = "invoices"
        ordering = ('id', 'inv_date', 'inv_nbr', 'date_paid')
        unique_together = ('id', )
        managed = True
