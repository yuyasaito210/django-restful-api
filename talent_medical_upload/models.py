from django.db import models
from talent.models import Talent
from client.models import Client


class TalentMedicalUpload(models.Model):
    talent = models.ForeignKey(Talent, related_name='talent_talent_medical_uploads', on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=True, blank=True)
    path = models.TextField(blank=True, null=True)
    preview_path = models.CharField(max_length=120, null=True, blank=True)
    url = models.TextField(blank=True, null=True)
    size = models.BigIntegerField(default=0)
    file_type = models.CharField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    uploaded = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return 'talent: {user_email}, image: {image_url}, {image_size}'.format(
            user_email=self.talent.user.email,
            image_url=self.url,
            image_size=self.size
        )

    class Meta:
        db_table = "talent_medical_upload"
        ordering = (
            'talent', 
            'updated', 
            'name'
        )
        managed = True
