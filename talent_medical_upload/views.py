import boto
import boto3
import mimetypes
import json
import time
import os
import sys
from datetime import datetime
from werkzeug.utils import secure_filename
from django.shortcuts import render
from django.http import Http404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from rest_framework import permissions, status, authentication
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from config.config_aws import (
    AWS_UPLOAD_BUCKET,
    AWS_UPLOAD_REGION,
    AWS_UPLOAD_ACCESS_KEY_ID,
    AWS_UPLOAD_SECRET_KEY,
    AWS_UPLOAD_RESUMES_PATH
)
from utils.aws_s3 import upload_medical_to_aws_s3
from .models import TalentMedicalUpload
from .serializers import TalentMedicalUploadSerializer
from talent.models import Talent
from authentication.models import User
from utils.text2pdf import text_to_image
from utils.pdf2jpg import pdf_to_image
from utils.doc2pdf import doc_to_pdf, docx_to_pdf
from user_note.models import UserNoteManager

ALLOWED_EXTENSIONS = set(['pdf'])


class TalentMedicalUploadFileUploadPolicy(APIView):
    """
    This view is to get the AWS Upload Policy for images to s3 bucket.
    What we do here is first create a TalentMedicalUpload object instance in ShipTalent
    backend. This is to include the TalentMedicalUpload instance in the path
    we will use within our bucket as you'll see below.
    """
    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            talent = Talent.objects.get(user=user.id)
            return talent
        except Talent.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        conn = boto.connect_s3(AWS_UPLOAD_ACCESS_KEY_ID, AWS_UPLOAD_SECRET_KEY)

        object_name = request.data.get('objectName')
        content_type = request.data.get('contentType') #mimetypes.guess_type(object_name)[0]
        if not object_name:
            return Response({"message": "A filename is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not content_type:
            return Response({"message": "A content type is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate bucket sub url
        policy_expires = int(time.time()+5000)
        talent = self.get_object(pk)
        talent_id = talent.id
        user_id = talent.user.username
        talent_medicals = TalentMedicalUpload.objects.filter(talent=talent)
        print('==== talent_medicals: ', talent_medical_uploads)
        print('==== talent.talent_medicals.count: ', len(talent_medicals))
        if len(talent_medicals) > 0:
          talent_medical = talent_medicals.first()
        else:
          talent_medical = TalentMedicalUpload.objects.create(talent=talent, name=object_name)

        talent_medical_upload_id = talent_medical_upload.id
        _, file_extension = os.path.splitext(object_name)
        
        upload_start_path = "{medicals_path}/{talent_id}/".format(
                medicals_path=AWS_UPLOAD_MEDICALS_PATH,
                talent_id = talent_id,
                talent_medical_upload_id=talent_medical_upload_id,
                file_extension=file_extension
            )
        filename_final = "{talent_medical_upload_id}{file_extension}".format(
                talent_medical_upload_id= talent_medical_upload_id,
                file_extension=file_extension
            )
 
        # Save signed url
        """
        Eventual file_upload_path includes the renamed file to the 
        Django-stored TalentMedicalUpload instance ID. Renaming the file is 
        done to prevent issues with user generated formatted names.
        """
        final_upload_path = "{upload_start_path}{filename_final}".format(
                upload_start_path=upload_start_path,
                filename_final=filename_final,
            )

        upload_url = "https://{bucket_name}.s3.amazonaws.com/{final_upload_path}".format(
                bucket_name=AWS_UPLOAD_BUCKET,
                final_upload_path=final_upload_path
            )

        # get signed url from AWS S3
        signed_url = conn.generate_url(
            300,
            "PUT",
            AWS_UPLOAD_BUCKET,
            final_upload_path,
            headers = {'Content-Type': content_type, 'x-amz-acl':'public-read'})

        if object_name and file_extension:
            """
            Save the eventual path to the Django-stored TalentMedicalUpload instance
            """
            talent_medical_upload.path = final_upload_path
            talent_medical_upload.url = upload_url
            talent_medical_upload.file_type = file_extension
            talent_medical_upload.save()

        data = {
            'signedUrl': signed_url,
            'fileID': talent_medical_upload_id
        }
        return Response(data, status=status.HTTP_200_OK)


class FileUploadCompleteHandler(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [authentication.SessionAuthentication]
    # Save uploaded file path and mark active state of it.
    """
    Save uploaded file path and mark active state of it.
    """
    def post(self, request, *args, **kwargs):
        file_id = request.data.get('fileID')
        size = request.data.get('fileSize')
        course_obj = None
        data = {}
        file_type = request.data.get('fileType')
        tmp = file_type.split('/')
        file_type = tmp[len(tmp) - 1]
        print(file_id, size, file_type)
        if file_id:
            obj = TalentMedicalUpload.objects.get(id=int(file_id))
            obj.size = int(size)
            obj.uploaded = True
            # obj.file_type = file_type
            obj.save()
            data['id'] = obj.id
            data['saved'] = True

            # Logging
            talent_user = obj.talent.user
            UserNoteManager.profile_logger(
                None, None, talent_user,
                '{user} uploaded resume.'.format(user=talent_user.first_name),
                obj
            )

        return Response(data, status=status.HTTP_200_OK)


class TalentMedicalUploadGeneratePrevew(APIView):
    parser_class = (FileUploadParser,)
    height = 1024
    width = 526
    page_id = 1

    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            talent = Talent.objects.get(user=user.id)
            return talent
        except Talent.DoesNotExist:
            raise Http404
 

    def convert_pdf_to_image(self, cach_dir_path, file_path):
        return pdf_to_image(cach_dir_path, file_path)

    def convert_text_to_png(self, file_path):
        file_name, file_extension = os.path.splitext(file_path)
        image_file_name = '{file_name}{extension}'.format(
                file_name = file_name,
                extension = '.png'
            )
        image = text_to_image(file_path)
        image.save(image_file_name)
        return image_file_name

    def convert_doc_to_pdf(self, file_path):
        preview = doc_to_pdf(file_path)
        return preview

    def convert_docx_to_pdf(self, file_path):
        preview = docx_to_pdf(file_path)
        return preview


    """
    Generate preview resume file in pdf, doc, docx format files and return image path.
    """   
    def put(self, request, pk, format=None):
        talent = self.get_object(pk)

        if 'file' not in request.data:
            raise ParseError("Empty content")

        if not talent:
            raise ParseError("Not found the talent or user")

        # Save temp file
        f = request.data['file']

        file_name = secure_filename('{filename}_{strdate}'.format(
            filename=request.data['fileName']),
            strdate=datetime.now().strftime("%m%d%Y%H%M%S")
        )
        file_id = request.data['fileID']
        tmp_file_dir = 'medicals/{talent_id}/'.format(
                talent_id = talent.id
            )
        tmp_file_path = '{tmp_file_dir}/{file_name}'.format(
                tmp_file_dir = tmp_file_dir,
                file_name = file_name
            )
        stored_path = default_storage.save(tmp_file_path, ContentFile(f.read()))

        # Generate preview file in image file
        media_root = settings.MEDIA_ROOT
        full_dir = os.path.join(media_root, tmp_file_dir)
        full_path = os.path.join(media_root, stored_path)

        # Get extension
        _, file_extension = os.path.splitext(stored_path)
        if sys.platform == 'darwin':
            if file_extension == '.txt':
                preview = self.convert_text_to_png(full_path)
            elif file_extension == '.doc':
                preview = self.convert_doc_to_pdf(full_path)
                preview = self.convert_pdf_to_image(full_dir, preview)
            elif file_extension == '.docx':
                preview = self.convert_docx_to_pdf(full_path)
                preview = self.convert_pdf_to_image(full_dir, preview)
            elif file_extension == '.pdf':
                preview = self.convert_pdf_to_image(full_dir, full_path)
        else:
            preview = self.convert_pdf_to_image(full_dir, full_path)

        # tmp = preview.split('/')
        # preview_file_name = tmp[len(tmp) - 1]
        # preview_file_path = os.path.join('media', tmp_file_dir, preview_file_name)
        
        # Upload preview_file
        uploaded_s3_url = upload_medical_to_aws_s3(preview, file_name)
        # Save generated preview image file path
        data = {}
        obj = TalentMedicalUpload.objects.get(id=int(file_id))
        obj.uploaded = True
        obj.preview_path = uploaded_s3_url
        obj.save()
        data['id'] = obj.id
        data['preview_path'] = uploaded_s3_url
        
        return Response(data, status=status.HTTP_200_OK)


class TalentMedicalUploadList(APIView):
    """
    List all talent resumes.
    """

    def get(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
            talent = Talent.objects.get(user=user.id)
            talent_medical_uploads = TalentMedicalUpload.objects.filter(talent=talent.id)
            serializer = TalentMedicalUploadSerializer(talent_medical_uploads, many=True)
            return Response(serializer.data)
        except Talent.DoesNotExist:
            raise Http404

class TalentMedicalUploadDetail(APIView):
    """
    Retrieve a talent picture instance.
    """
    def get_object(self, pk):
        try:
            return TalentMedicalUpload.objects.get(pk=pk)
        except TalentMedicalUpload.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        talent_medical_upload_item = self.get_object(pk)
        serializer = TalentMedicalUploadSerializer(talent_medical_upload_item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        talent_medical_upload_item = self.get_object(pk)
        serializer = TalentMedicalUploadSerializer(talent_medical_upload_item, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Logging
            user = request.user
            if user and 'approved' in serializer.data:
                talent_user = talent_medical_upload_item.talent.user
                UserNoteManager.profile_logger(
                    None, user, talent_user, 
                    'Resume of {talent} {status} by {user}.'.format(
                        talent=talent_user.first_name,
                        status='Approved' if serializer.data['approved'] else 'Rejected',
                        user=user.first_name
                    ),
                    talent_medical_upload_item
                )

            return Response(serializer.data)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        talent_medical_upload_item = self.get_object(pk)
        talent_medical_upload_item.delete()

        user = request.user
        if user:
            talent_user = talent_medical_upload_item.talent.user
            note = ''
            if user.type == 'agency':
                note = 'Resume of {talent} {status} by {user}. Comment: {comment}'.format(
                    talent=talent_user.first_name,
                    status='Rejected',
                    user=user.first_name,
                    comment= request.data['comment'] if 'comment' in request.data else ''
                )
            elif user.type == 'talent':
                note = '{user} removed resume.'.format(user=user.first_name)

            UserNoteManager.profile_logger(None, user, talent_user, note, talent_medical_upload_item)

        return Response({'id': pk}, status=status.HTTP_204_NO_CONTENT)