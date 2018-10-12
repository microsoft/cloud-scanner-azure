import os

from cloud_scanner.contracts import ResourceServiceFactory
from .unittest_base import TestCase


class TestResourceServiceFactory(TestCase):

    def test_azure_provider(self):
        os.environ["AZURE_CLIENT_ID"] = "00000000-0000-0000-0000-000000000000"
        os.environ["AZURE_CLIENT_SECRET"] = "*****"
        os.environ["AZURE_TENANT_ID"] = "00000000-0000-0000-0000-000000000000"

        service = ResourceServiceFactory.create("azure", "00000000-0000-0000-0000-000000000000")
        self.assertFalse(service is None)
        self.assertEqual("AzureResourceService", type(service).__name__)

    def test_simulator_provider(self):
        service = ResourceServiceFactory.create("simulator", "00000000-0000-0000-0000-000000000000")
        self.assertFalse(service is None)
        self.assertEqual("ResourceServiceSimulator", type(service).__name__)

    def test_unknown_provider(self):
        test_error = None

        try:
            ResourceServiceFactory.create("unknown", None)
        except Exception as create_error:
            test_error = create_error

        self.assertFalse(test_error is None, "Expected error to be thrown for invalid provider")
