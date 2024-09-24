import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, status
import logging
from br_common.enums import ErrorMessages
from br_common.utils import CoreUtils
import os

# https://aws.amazon.com/developer/language/python/

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class SecretManagerService:
    """
    Service class to interact with AWS Secrets Manager.
    """

    def __init__(self):
        self.client = boto3.client("secretsmanager")

    def get_secret(self, secret_name: str):
        """
        Retrieve a secret value from AWS Secrets Manager.
        """
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            if "SecretString" in response:
                return response["SecretString"]
            else:
                return response["SecretBinary"]
        except ClientError as e:
            logger.error(f"Failed to retrieve secret {secret_name}: {e}")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=CoreUtils.format_error_response(
                    ErrorMessages.AWS_SECRET_EXCEPTION.name,
                    ErrorMessages.AWS_SECRET_EXCEPTION.value,
                ),
            )


class SESService:
    """
    Service class to interact with AWS Simple Email Service (SES) for sending emails.
    """

    def __init__(self):
        """
        Initialize the SES client.
        """
        self.client = boto3.client("ses")

    def send_email(
        self,
        sender: str,
        recipient: str,
        subject: str,
        body_text: str,
        body_html: str = None,
    ):
        """
        Sends an email using Amazon SES.

        :param sender: Email address of the sender.
        :param recipient: Email address of the recipient.
        :param subject: Subject of the email.
        :param body_text: Text version of the email body.
        :param body_html: Optional HTML version of the email body.
        """
        try:
            # Construct the email payload
            message = {
                "Subject": {"Data": subject, "Charset": "UTF-8"},
                "Body": {"Text": {"Data": body_text, "Charset": "UTF-8"}},
            }

            # If HTML body is provided, add it to the message
            if body_html:
                message["Body"]["Html"] = {"Data": body_html, "Charset": "UTF-8"}

            # Send the email using SES
            response = self.client.send_email(
                Source=sender,
                Destination={
                    "ToAddresses": [recipient],
                },
                Message=message,
            )

            logger.info(f"Email sent successfully to {recipient}: {response}")
            return response

        except ClientError as e:
            logger.error(f"Failed to send email to {recipient}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=CoreUtils.format_error_response(
                    ErrorMessages.AWS_SES_EXCEPTION.name,
                    ErrorMessages.AWS_SES_EXCEPTION.value,
                ),
            )


class S3Service:
    """
    Service class to interact with AWS S3 for managing files and folders.
    """

    def __init__(self, bucket_name: str):
        """
        Initialize the S3 client and specify the bucket name.
        """
        self.bucket_name = bucket_name
        self.region_name = self.get_bucket_region()

        # Initialize the S3 client with the correct region
        self.s3_client = boto3.client(
            "s3",
            region_name=self.region_name,
            endpoint_url=f"https://s3.{self.region_name}.amazonaws.com",
        )

    def get_bucket_region(self) -> str:
        """
        Retrieves the region name of the S3 bucket.
        """
        try:
            response = boto3.client("s3").get_bucket_location(Bucket=self.bucket_name)
            region = response["LocationConstraint"]
            return "us-east-1" if region is None else region
        except ClientError as e:
            logger.error(
                f"Failed to retrieve region for bucket '{self.bucket_name}': {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=CoreUtils.format_error_response(
                    ErrorMessages.AWS_S3_BUCKET_REGION_ERROR.name,
                    ErrorMessages.AWS_S3_BUCKET_REGION_ERROR.value,
                ),
            )

    def create_folder(self, folder_path: str):
        """
        Creates a folder in the S3 bucket.

        :param folder_path: The path of the folder to create (e.g., "folder1/subfolder2/")
        """
        try:
            # Creating an empty object to represent the folder
            self.s3_client.put_object(Bucket=self.bucket_name, Key=f"{folder_path}/")
            logger.info(
                f"Folder '{folder_path}' created successfully in bucket {self.bucket_name}"
            )
        except ClientError as e:
            logger.error(f"Failed to create folder '{folder_path}': {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=CoreUtils.format_error_response(
                    ErrorMessages.AWS_S3_FOLDER_CREATE_ERROR.name,
                    ErrorMessages.AWS_S3_FOLDER_CREATE_ERROR.value,
                ),
            )

    def delete_folder(self, folder_path: str):
        """
        Deletes a folder from the S3 bucket.

        :param folder_path: The path of the folder to delete (e.g., "folder1/subfolder2/")
        """
        try:
            # Retrieve all objects under the folder and delete them
            objects_to_delete = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name, Prefix=folder_path
            )
            if "Contents" in objects_to_delete:
                delete_keys = [
                    {"Key": obj["Key"]} for obj in objects_to_delete["Contents"]
                ]
                self.s3_client.delete_objects(
                    Bucket=self.bucket_name, Delete={"Objects": delete_keys}
                )
                logger.info(
                    f"Folder '{folder_path}' and its contents have been deleted successfully."
                )
            else:
                logger.info(f"Folder '{folder_path}' does not exist.")
        except ClientError as e:
            logger.error(f"Failed to delete folder '{folder_path}': {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=CoreUtils.format_error_response(
                    ErrorMessages.AWS_S3_FOLDER_DELETE_ERROR.name,
                    ErrorMessages.AWS_S3_FOLDER_DELETE_ERROR.value,
                ),
            )

    def check_path_exists(self, s3_path: str) -> bool:
        """
        Check if a path exists in S3.

        :param s3_path: The path to check (e.g., "folder1/image.png" or "folder1/")
        :return: True if the path exists, False otherwise
        """
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_path)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            else:
                logger.error(f"Error checking if path '{s3_path}' exists: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=CoreUtils.format_error_response(
                        ErrorMessages.AWS_S3_EXCEPTION.name,
                        ErrorMessages.AWS_S3_EXCEPTION.value,
                    ),
                )

    def upload_file(self, file_path: str, s3_path: str):
        """
        Uploads a file to S3.

        :param file_path: The local path of the file to upload
        :param s3_path: The target path in the S3 bucket (e.g., "folder1/image.png")
        """
        try:
            self.s3_client.upload_fileobj(file_path, self.bucket_name, s3_path)
            logger.info(
                f"File '{file_path}' uploaded successfully to '{s3_path}' in bucket {self.bucket_name}"
            )
            return s3_path
        except ClientError as e:
            logger.error(f"Failed to upload file '{file_path}' to '{s3_path}': {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=CoreUtils.format_error_response(
                    ErrorMessages.AWS_S3_FILE_UPLOAD_ERROR.name,
                    ErrorMessages.AWS_S3_FILE_UPLOAD_ERROR.value,
                ),
            )

    def upload_file_or_create_path(self, file_path: str, s3_path: str):
        """
        Uploads a file to the specified path, creating the path if it doesn't exist.

        :param file_path: The local path of the file to upload
        :param s3_path: The target path in the S3 bucket (e.g., "folder1/image.png")
        """
        # Extract the directory path from the S3 path
        directory_path = os.path.dirname(s3_path) + "/"

        # Check if the directory path exists; if not, create it
        if not self.check_path_exists(directory_path):
            self.create_folder(directory_path)

        # Upload the file to the S3 path
        return self.upload_file(file_path, s3_path)

    def generate_presigned_url(self, s3_path: str, expiration=3600) -> str:
        """
        Generate a pre-signed URL for an S3 object.

        :param s3_path: The path of the file in S3 (e.g., "folder1/image.png")
        :param expiration: Time in seconds for the URL to remain valid (default: 1 hour)
        :return: The pre-signed URL as a string
        """
        try:
            # Ensure that the S3 client is initialized with the correct region
            presigned_url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": s3_path},
                ExpiresIn=expiration,
            )
            return presigned_url
        except ClientError as e:
            logger.error(f"Failed to generate pre-signed URL for '{s3_path}': {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=CoreUtils.format_error_response(
                    ErrorMessages.AWS_S3_PRESIGNED_URL_ERROR.name,
                    ErrorMessages.AWS_S3_PRESIGNED_URL_ERROR.value,
                ),
            )
