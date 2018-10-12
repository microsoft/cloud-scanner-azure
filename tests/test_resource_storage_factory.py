import os

from cloud_scanner.contracts.resource_storage_factory import ResourceStorageFactory
from .unittest_base import TestCase


class TestResourceStorageFactory(TestCase):
    def test_azure_cosmos_db_storage(self):
        os.environ["RESOURCE_STORAGE_TYPE"] = "azure_cosmos_table"
        os.environ["AZURE_COSMOS_TABLE"] = "test-table"
        os.environ["AZURE_COSMOS_ACCOUNT"] = "test-account"
        os.environ["AZURE_COSMOS_KEY"] = "******************"

        resource_storage = ResourceStorageFactory.create()
        self.assertIsNotNone(resource_storage)
        self.assertEqual(type(resource_storage).__name__, "AzureCosmosDb")

    def test_simulator_resource_storage(self):
        os.environ["RESOURCE_STORAGE_TYPE"] = "simulator"

        resource_storage = ResourceStorageFactory.create()
        self.assertIsNotNone(resource_storage)
        self.assertEqual(type(resource_storage).__name__, "TableStorageSimulator")
