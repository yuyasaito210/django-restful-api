"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog//', include('blog.urls'))
"""
# from django.urls import include, re_path
from django.conf.urls import include, url
from django.contrib import admin

from django.views.generic.base import TemplateView
from django.conf import settings
from django.views.static import serve
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import renderers, response, schemas
from talent import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

swagger_schema_view = get_swagger_view(title='ShipTalent API')

schema_view = get_schema_view(
   openapi.Info(
      title="Shiptalent API",
      default_version='v1',
      description="RESTful API for www.shiptalent.com",
      terms_of_service="https://www.shiptalent.com/terms/",
      contact=openapi.Contact(email="administrator@shiptalent.com"),
      license=openapi.License(name="ShipTalent.com"),
   ),
   # validators=['flex', 'ssv'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
  url(r'^apis(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
  url(r'^apis/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
  url(r'^swagger-docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
  url(r'^django-admin/', admin.site.urls),
  url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
  url(r'^api/v1/auth/', include('authentication.urls')),
  url(r'^api/v1/talent/', include('talent.urls')),
  url(r'^api/v1/talent_position_type', include('talent_position_type.urls')),
  url(r'^api/v1/talent_position_sub_type/', include('talent_position_sub_type.urls')),
  url(r'^api/v1/talent_skill/', include('talent_skill.urls')),
  url(r'^api/v1/talent_sub_skill/', include('talent_sub_skill.urls')),
  url(r'^api/v1/talent_visa/', include('talent_visa.urls')),
  url(r'^api/v1/talent_language/', include('talent_language.urls')),
  url(r'^api/v1/talent_picture/', include('talent_picture.urls')),
  url(r'^api/v1/talent_resume/', include('talent_resume.urls')),
  url(r'^api/v1/talent_video/', include('talent_video.urls')),
  url(r'^api/v1/talent_medical/', include('talent_medical.urls')),
  url(r'^api/v1/talent_availability/', include('talent_availability.urls')),
  url(r'^api/v1/talent_rating/', include('talent_rating.urls')),
  url(r'^api/v1/talent_video_greetings/', include('talent_video_greeting.urls')),
  url(r'^api/v1/talent_video_sub_skills/', include('talent_video_sub_skill.urls')),
  url(r'^api/v1/position_type/', include('position_type.urls')),
  url(r'^api/v1/position_sub_type/', include('position_sub_type.urls')),
  url(r'^api/v1/skill/', include('skill.urls')),
  url(r'^api/v1/sub_skill/', include('sub_skill.urls')),
  url(r'^api/v1/question/', include('question.urls')),
  url(r'^api/v1/wizard_question/', include('wizard_question.urls')),
  url(r'^api/v1/wizard_question_answer/', include('wizard_question_answer.urls')),
  url(r'^api/v1/position_wizard_question_scenario/', include('position_wizard_question_scenario.urls')),
  url(r'^api/v1/shiptalent_info/', include('shiptalent_info.urls')),
  url(r'^api/v1/submission/', include('submission.urls')),
  url(r'^api/v1/video_interview_settings/', include('admin_setting.urls')),
  url(r'^api/v1/client/', include('client.urls')),
  url(r'^api/v1/client/casting_request/', include('casting_request.urls')),
  url(r'^api/v1/client/casting_request_talent/', include('casting_request_talent.urls')),
  url(r'^api/v1/client/blocked_profile/', include('blocked_profile.urls')),
  url(r'^api/v1/client/call_back/', include('call_back.urls')),
  url(r'^api/v1/client/favorite/', include('favorite.urls')),
  url(r'^api/v1/client/team/', include('team.urls')),
  url(r'^api/v1/client/team_member/', include('team_member.urls')),
  url(r'^api/v1/client/shared_profile/', include('shared_profile.urls')),
  url(r'^api/v1/client/feedback/', include('client_feedback.urls')),
  url(r'^api/v1/client/request/', include('client_request.urls')),
  url(r'^api/v1/agency/overview/', include('agency.overview.urls')),
  url(r'^api/v1/agency/casting_request/', include('agency.casting_request_urls')),
  url(r'^api/v1/agency/casting_request_talent/', include('agency.casting_request_talent_urls')),
  url(r'^api/v1/agency/user_note/', include('user_note.urls')),
  url(r'^api/v1/agency/talent_medical_upload/', include('talent_medical_upload.urls')),
  url(r'^api/v1/agency/invoice/', include('agency.invoice_urls')),
]
