import os

from cloud_scanner.contracts.storage_container_factory import StorageContainerFactory
from .unittest_base import TestCase


class TestStorageContainerFactory(TestCase):
    def setUp(self):
        pass
        os.environ["CONFIG_CONTAINER"] = "test-container"
        os.environ["AZURE_STORAGE_ACCOUNT"] = "test-account"
        os.environ["AZURE_STORAGE_KEY"] = "********"

    def test_create_azure_storage_provider(self):
        os.environ["STORAGE_CONTAINER_TYPE"] = "azure_storage"

        container = StorageContainerFactory.create()
        self.assertIsNotNone(container)
        self.assertEqual(type(container).__name__, "AzureStorageContainer")

    def test_create_container_simulator(self):
        os.environ["STORAGE_CONTAINER_TYPE"] = "simulator"

        container = StorageContainerFactory.create()
        self.assertIsNotNone(container)
        self.assertEqual(type(container).__name__, "MockBlobStorageSimulator")


