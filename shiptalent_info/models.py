from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime, timedelta

class ShipTalentInfoManager(models.Manager):
  def get_queryset(self):
    return super(ShipTalentInfoManager, self).get_queryset().filter(active=True)

class ShipTalentInfo(models.Model):
  name = models.CharField(max_length=50, blank=False, default='')
  value = models.TextField(default='', blank=False)
  description = models.CharField(max_length=100, blank=True, default='')
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    """
    Returns a string representation of this `ShipTalentInfo`.
    This string is used when a `ShipTalentInfo` is printed in the console.
    """
    return self.name

  class Meta:
    db_table = "shiptalent_info"
    ordering = ('name',)
    managed = True
