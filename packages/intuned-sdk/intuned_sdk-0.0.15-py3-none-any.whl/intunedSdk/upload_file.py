import os
import uuid
from botocore.exceptions import NoCredentialsError
from boto3 import client
from boto3.s3.transfer import TransferConfig
from botocore.client import Config

from typing import Union, Optional
from pathlib import Path
from playwright.async_api import Download

from typing import TypedDict
from dotenv import load_dotenv
from dataclasses import dataclass

from .utils.get_mode import is_generate_code_mode
from .utils.get_s3_client import get_s3_client

load_dotenv()


@dataclass
class UploadedFile:
    file_name: str
    bucket: str

    def get_signed_url(self, expiration: int = 3600):
        if is_generate_code_mode():
            return f"https://{self.bucket}.s3.amazonaws.com/{self.file_name}"
        s3_client = get_s3_client()

        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": self.file_name},
            ExpiresIn=expiration,
        )
        return response

    def get_s3_key(self):
        return f"s3://{self.bucket}/{self.file_name}"



class UploadFileToS3Configs(TypedDict):
    endpoint: Optional[str]
    fileNameOverride: Optional[str]


FileType = Union[Download, str, bytes]


async def upload_file_to_s3(
    file: FileType,
    endpoint: Optional[str] = None,
    fileNameOverride: Optional[str] = None,
) -> UploadedFile:
    is_downloaded_file = isinstance(file, Download)

    if is_downloaded_file and not await file.path():
        raise ValueError("File path not found")

    if is_generate_code_mode():
        print("Uploaded file successfully")
        return UploadedFile(
            file_name=fileNameOverride or str(uuid.uuid4()),
            bucket=os.environ.get("INTUNED_S3_BUCKET"),
        )

    s3_client = get_s3_client(endpoint)

    file_body = await get_file_body(file)
    suggested_file_name = file.suggested_filename if is_downloaded_file else None

    file_name = (
        fileNameOverride
        if fileNameOverride is not None
        else suggested_file_name or str(uuid.uuid4())
    )

    bucket_name = os.environ.get("INTUNED_S3_BUCKET")

    try:
        response = s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=file_body,
        )
    except NoCredentialsError:
        raise Exception("Credentials not available")

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return UploadedFile(
            file_name,
            bucket_name,
        )
    else:
        raise Exception("Error uploading file")


async def get_file_body(file: FileType):
    if isinstance(file, Download):
        file_path = await file.path()
        if not file_path:
            raise ValueError("Downloaded file path not found")
        with open(file_path, "rb") as f:
            return f.read()
    return file
