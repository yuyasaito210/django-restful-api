from django.db import models


class PositionTypeManager(models.Manager):
    def get_queryset(self):
        return super(PositionTypeManager, self).get_queryset().filter(active=True)


class PositionType(models.Model):
    name = models.CharField(blank=False, max_length=50)
    abbreviated_key = models.CharField(max_length=1, blank=True)
    priority = models.IntegerField(blank=True, default=100)
    multi_selection = models.BooleanField(default=False)
    select_option_title = models.CharField(blank=True, max_length=100, default='')
    wizard_button_title = models.CharField(blank=True, max_length=100, default='')
    agent_title = models.CharField(blank=True, max_length=100, default='')
    video_audition_button_title = models.CharField(blank=True, max_length=100, default='')
    question = models.TextField(max_length=300, blank=True)
    introduction_link = models.CharField(blank=True, max_length=1024)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "position_type"
        ordering = ('priority', 'name',)
        managed = True
        unique_together = ('name', 'id')
