import os

from cloud_scanner.contracts import AccountServiceFactory
from .unittest_base import TestCase


class TestAccountServiceFactory(TestCase):
    def test_azure_account_service(self):
        os.environ["AZURE_CLIENT_ID"] = "00000000-0000-0000-0000-000000000000"
        os.environ["AZURE_CLIENT_SECRET"] = "*****"
        os.environ["AZURE_TENANT_ID"] = "00000000-0000-0000-0000-000000000000"

        account_service = AccountServiceFactory.create("azure")
        self.assertIsNotNone(account_service)
        self.assertEqual(type(account_service).__name__, "AzureSubscriptionService")

    def test_simulator_account_service(self):
        account_service = AccountServiceFactory.create("simulator")
        self.assertIsNotNone(account_service)
        self.assertEqual(type(account_service).__name__, "AccountServiceSimulator")
