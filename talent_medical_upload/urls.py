from django.views.generic.base import TemplateView
from .views import FileUploadCompleteHandler, TalentMedicalUploadFileUploadPolicy, TalentMedicalUploadList, TalentMedicalUploadDetail
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
  url(r'^upload/(?P<pk>[0-9]+)/complete/', FileUploadCompleteHandler.as_view(), name='upload-complete'),
  url(r'^upload/(?P<pk>[0-9]+)/policy/', TalentMedicalUploadFileUploadPolicy.as_view()),
  url(r'^upload/(?P<pk>[0-9]+)/medicals/', TalentMedicalUploadList.as_view()),
  url(r'^(?P<pk>[0-9]+)/', TalentMedicalUploadDetail.as_view())
]