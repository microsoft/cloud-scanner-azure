from azure.storage.blob.blockblobservice import BlockBlobService
from cloud_scanner.config import ProcessConfig
from cloud_scanner.contracts import (
    StorageContainer, register_storage_container
)

from cloud_scanner_azure.config.azure_config import AzureConfig
from cloud_scanner_azure.config.azure_storage_config import AzureStorageConfig


@register_storage_container("azure_storage",
                            lambda: AzureStorageContainer.create())
class AzureStorageContainer(StorageContainer):
    """Azure implementation of Storage Container using BlockBlobService."""

    def __init__(self, container_name, config: AzureStorageConfig):
        self._blob_service = None
        self._container_name = container_name
        self._config = config

    def _get_client(self):
        """
        :return: BlockBlobService initialized with account
        name and key from config
        """
        if self._blob_service is None:
            self._blob_service = BlockBlobService(
                account_name=self._config.account_name,
                account_key=self._config.account_key
            )

            self._blob_service.create_container(self._container_name)

        return self._blob_service

    def upload_text(self, blob_name, text):
        """Uploads text to a new blob.

        :param blob_name: Name to give new blob
        :param text: Text to upload
        :return: None
        """
        self._get_client().create_blob_from_text(self._container_name,
                                                 blob_name, text)

    def list_blobs(self):
        """List all blobs in container.

        :return: List of blobs in container
        """
        return self._get_client().list_blobs(self._container_name)

    def get_blob_to_text(self, file_name):
        """Get string from contents of blob.

        :param file_name: Name of blob file
        :return: Text from blob file
        """
        return self._get_client().get_blob_to_text(self._container_name,
                                                   file_name)

    @staticmethod
    def create():
        """Initialize AzureStorageContainer with name and creds from config.

        :return:
        """
        return AzureStorageContainer(
            ProcessConfig().config_container_name,
            AzureConfig().storage_config)
