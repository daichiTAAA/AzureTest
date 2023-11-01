"""Azure Data Lake Storage (ADLS) class.
This class provides methods to interact with ADLS Gen2.
"""
import os

from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

import settings


class ADLS:
    def __init__(self):
        """Initialize the ADLS Gen2 class."""
        print("settings.ENV", settings.ENV)
        if settings.ENV == "LOCAL":
            account_url = (
                f"https://{settings.STORAGE_ACCOUNT_NAME}.dfs.core.windows.net"
            )
            self.service_client = DataLakeServiceClient(
                account_url, credential=settings.SAS_TOKEN
            )
        else:
            account_url = (
                f"https://{os.environ['STORAGE_ACCOUNT_NAME']}.dfs.core.windows.net"
            )
            token_credential = DefaultAzureCredential()
            self.service_client = DataLakeServiceClient(
                account_url, credential=token_credential
            )

    def get_files_in_directory(self, file_system_name, directory_name):
        """Get the files in a directory.
        Args:
            file_system_name (str): The name of the file system.
            directory_name (str): The name of the directory.
        Returns:
            list: A list of the files in the directory.
        """
        file_system_client = self.service_client.get_file_system_client(
            file_system=file_system_name
        )
        paths = file_system_client.get_paths(path=directory_name)
        return [path.name for path in paths]
