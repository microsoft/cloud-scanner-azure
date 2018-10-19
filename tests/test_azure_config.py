import os

from cloud_scanner_azure.config import AzureConfig
from .unittest_base import TestCase 


class TestAzureConfig(TestCase):
    def test_get_property(self):
        expected_client_id = "XXXXXXX"
        os.environ["AZURE_CLIENT_ID"] = expected_client_id

        config = AzureConfig()
        actual_client_id = config.get_property("CLIENT_ID")

        self.assertEqual(expected_client_id, actual_client_id)

    def test_credential_config(self):
        client_id = "TEST_CLIENT_ID"
        client_secret = "TEST_CLIENT_SECRET"
        tenant_id = "TEST_TENANT_ID"

        os.environ["AZURE_CLIENT_ID"] = client_id
        os.environ["AZURE_CLIENT_SECRET"] = client_secret
        os.environ["AZURE_TENANT_ID"] = tenant_id

        config = AzureConfig()
        credential_config = config.credential_config

        self.assertEqual(client_id, credential_config.client_id)
        self.assertEqual(client_secret, credential_config.client_secret)
        self.assertEqual(tenant_id, credential_config.tenant_id)


