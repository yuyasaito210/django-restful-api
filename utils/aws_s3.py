import boto3
from config.config_aws import (
    AWS_UPLOAD_BUCKET,
    AWS_UPLOAD_REGION,
    AWS_UPLOAD_ACCESS_KEY_ID,
    AWS_UPLOAD_SECRET_KEY,
    AWS_UPLOAD_VIDEOS_PATH,
    AWS_UPLOAD_RESUMES_PATH,
    AWS_UPLOAD_MEDICALS_PATH
)


def upload_file_to_aws_s3(file_path, bucket_name, branch_path, file_name):
  session = boto3.Session(
      aws_access_key_id=AWS_UPLOAD_ACCESS_KEY_ID,
      aws_secret_access_key='AWS_SECRET_ACCESS_KEY',
  )
  s3 = session.resource('s3')
  upload_path = '{branch_path}/{file_name}'.format(
      branch_path=branch_path, 
      file_name=file_name
    )
  s3.meta.client.upload_file(
    Filename=file_path, 
    Bucket=AWS_UPLOAD_BUCKET, 
    Key=upload_path
  )

  return "https://{bucket_name}.s3.amazonaws.com/{upload_path}".format(
                bucket_name=bucket_name,
                upload_path=upload_path
            )

def upload_medical_to_aws_s3(file_path, file_name):
  return upload_file_to_aws_s3(file_path, AWS_UPLOAD_BUCKET, AWS_UPLOAD_MEDICALS_PATH, file_name)