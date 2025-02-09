import boto3
from django.conf import settings
from django.core.exceptions import ValidationError

from shop.settings import AWS_LOCAL_STORAGE
import uuid


class Bucket:
    """
    CDN bucket manager
    init method creates connection
    NOTE:
        none of these methods are async .use public interface it task.py module instead
    """

    def __init__(self):
        session = boto3.session.Session()
        self.conn = session.client(
            service_name=settings.AWS_SERVICE_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        )

    def get_objects(self):
        response = self.conn.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        if response.get('KeyCount') > 0:
            return response['Contents']
        else:
            return None

    def delete_object(self, key):
        response = self.conn.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key,
        )
        return True

    def download_object(self, key):
        with open(AWS_LOCAL_STORAGE + key, "wb") as f:
            self.conn.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, f, key)

    def upload_object(self, file_obj, filename):

        self.conn.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            ACL='private',
            Body=file_obj,
            Key=filename,

        )


bucket = Bucket()
