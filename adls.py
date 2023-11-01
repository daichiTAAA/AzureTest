"""Azure Data Lake Storage (ADLS) class.
This class provides methods to interact with ADLS.
"""
import os

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


class ADLS:
    def __init__(self):
        """Initialize the ADLS class."""
        # Acquire a credential object
        token_credential = DefaultAzureCredential()
        storage_account_name = os.environ["STORAGE_ACCOUNT_NAME"]
        self.blob_service_client = BlobServiceClient(
            account_url=f"https://{storage_account_name}.blob.core.windows.net",
            credential=token_credential,
        )

    def get_blob(self, container_name, blob_name):
        """Get a blob from a container.
        :param container_name: Name of the container.
        :type container_name: str
        :param blob_name: Name of the blob.
        :type blob_name: str
        :return: The blob data.
        :rtype: bytes
        """
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.download_blob().readall()

    def get_blob_names(self, container_name):
        """Get a list of blob names from a container.
        :param container_name: Name of the container.
        :type container_name: str
        :return: List of blob names.
        :rtype: list[str]
        """
        container_client = self.blob_service_client.get_container_client(container_name)
        return [blob.name for blob in container_client.list_blobs()]

    def get_container_names(self):
        """Get a list of container names.
        :return: List of container names.
        :rtype: list[str]
        """
        return [
            container.name for container in self.blob_service_client.list_containers()
        ]

    def get_containers(self):
        """Get a list of containers.
        :return: List of containers.
        :rtype: list[azure.storage.blob.ContainerProperties]
        """
        return self.blob_service_client.list_containers()

    def upload_blob(self, container_name, blob_name, data):
        """Upload a blob to a container.
        :param container_name: Name of the container.
        :type container_name: str
        :param blob_name: Name of the blob.
        :type blob_name: str
        :param data: The data to upload.
        :type data: bytes
        """
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data)
