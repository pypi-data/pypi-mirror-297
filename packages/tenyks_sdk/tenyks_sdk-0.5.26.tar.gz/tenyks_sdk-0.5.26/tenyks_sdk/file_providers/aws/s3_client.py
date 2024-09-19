import logging
from io import BytesIO
from typing import Any, Dict, List

from botocore.client import BaseClient

logger = logging.getLogger(__name__)


class S3Client:
    def __init__(self, boto3_s3_client: BaseClient) -> None:
        self.boto3_s3_client = boto3_s3_client

    def list_objects_v2(self, s3_bucket: str, prefix: str) -> list:
        try:
            paginator = self.boto3_s3_client.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=s3_bucket, Prefix=prefix)
            result = []
            for page in pages:
                result.extend(page.get("Contents", []))
            return result
        except Exception as e:
            logger.error(f"Error listing objects: {str(e)}")
            raise RuntimeError("Failed to list objects in S3")

    def get_object(self, s3_bucket: str, s3_key: str) -> object:
        try:
            return self.boto3_s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
        except Exception as e:
            logger.error(f"Error getting object: {str(e)}")
            raise RuntimeError("Failed to get object from S3")

    def head_object(self, s3_bucket: str, s3_key: str) -> object:
        try:
            return self.boto3_s3_client.head_object(Bucket=s3_bucket, Key=s3_key)
        except Exception as e:
            logger.error(f"Error heading object: {str(e)}")
            raise RuntimeError("Failed to head object in S3")

    def generate_presigned_url(
        self,
        s3_bucket: str,
        s3_key: str,
        expires_in: int,
    ):
        try:
            return self.boto3_s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": s3_bucket,
                    "Key": s3_key,
                },
                ExpiresIn=expires_in,
            )
        except Exception as e:
            logger.error(f"Error generating presigned URL: {str(e)}")
            raise RuntimeError("Failed to generate presigned URL")

    def upload_fileobj(
        self,
        file_stream: BytesIO,
        s3_bucket: str,
        s3_key: str,
    ):
        try:
            self.boto3_s3_client.upload_fileobj(
                file_stream,
                Bucket=s3_bucket,
                Key=s3_key,
            )
        except Exception as e:
            logger.error(f"Error uploading file object: {str(e)}")
            raise RuntimeError("Failed to upload file object to S3")

    def delete_objects(self, s3_bucket: str, objects_to_delete: List[Dict[str, Any]]):
        objects_to_delete_chunks = self.__chunk_array(objects_to_delete, 1000)

        for objects_to_delete_chunk in objects_to_delete_chunks:
            try:
                self.boto3_s3_client.delete_objects(
                    Bucket=s3_bucket, Delete={"Objects": objects_to_delete_chunk}
                )
            except Exception as e:
                logger.error(f"Error deleting objects: {str(e)}")
                raise RuntimeError("Failed to delete objects from S3")

    def __chunk_array(self, arr, chunk_size):
        return [arr[i : i + chunk_size] for i in range(0, len(arr), chunk_size)]
