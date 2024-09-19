import logging
from datetime import timedelta
from io import BytesIO
from typing import List

from google.api_core import retry
from google.cloud.storage import Blob, Client

retry_wrapper = retry.Retry(predicate=retry.if_transient_error)

logger = logging.getLogger(__name__)


class GCSClient:
    def __init__(self, client: Client) -> None:
        self.client = client

    @retry_wrapper
    def generate_url(
        self, bucket: str, bucket_internal_path: str, expiration_seconds: int
    ) -> str:
        try:
            blob = self.get_blob(bucket, bucket_internal_path)
            generated_url = blob.generate_signed_url(
                version="v4",
                expiration=timedelta(seconds=expiration_seconds),
                method="GET",
            )
            return generated_url
        except Exception as e:
            logger.error(f"Error generating URL: {str(e)}")
            raise RuntimeError("Failed to generate signed URL")

    def get_blob(self, bucket: str, bucket_internal_path: str) -> Blob:
        try:
            blob = self.client.bucket(bucket).get_blob(bucket_internal_path)
            return blob
        except Exception as e:
            logger.error(f"Error getting blob: {str(e)}")
            raise RuntimeError("Failed to get blob from GCS")

    def list_files(self, bucket: str, prefix: str) -> List[str]:
        try:
            blobs = self.client.list_blobs(bucket_or_name=bucket, prefix=prefix)
            file_paths_only = [
                blob.name for blob in blobs if not blob.name.endswith("/")
            ]
            return file_paths_only
        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
            raise RuntimeError("Failed to list files in GCS")

    def does_file_exist(self, bucket: str, bucket_internal_path: str) -> bool:
        try:
            matching_result = self.get_blob(bucket, bucket_internal_path)
            if matching_result is None:
                return False
            exists = matching_result.exists()
            return exists
        except Exception as e:
            logger.error(f"Error checking file existence: {str(e)}")
            raise RuntimeError("Failed to check file existence in GCS")

    @retry_wrapper
    def save_file(self, bucket: str, bucket_internal_path: str, file: BytesIO):
        try:
            new_blob = self.client.bucket(bucket).blob(bucket_internal_path)
            new_blob.upload_from_file(file)
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise RuntimeError("Failed to save file to GCS")

    @retry_wrapper
    def delete_file(self, bucket: str, bucket_internal_path: str):
        try:
            blob_to_delete = self.client.bucket(bucket).blob(bucket_internal_path)
            blob_to_delete.delete()
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            raise RuntimeError("Failed to delete file from GCS")

    @retry_wrapper
    def delete_by_prefix(self, bucket: str, prefix: str):
        try:
            blobs = self.client.list_blobs(bucket_or_name=bucket, prefix=prefix)
            for blob in blobs:
                blob.delete()
        except Exception as e:
            logger.error(f"Error deleting files by prefix: {str(e)}")
            raise RuntimeError("Failed to delete files by prefix from GCS")
