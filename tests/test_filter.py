from .unittest_base import TestCase
from cloud_scanner_azure.services.azure_resource_service import (
    AzureResourceService)


class TestFilter(TestCase):

    def test_no_filter(self):
        resource_service = AzureResourceService(None)
        f = resource_service.get_filter(None)
        self.assertEqual(f.normalized_filter(), None)

    def test_shorthand_filter(self):
        resource_service = AzureResourceService(None)
        f = resource_service.get_filter('vm')
        self.assertEqual(f.normalized_filter(), "resourceType eq 'Microsoft.Compute/virtualMachines'")
        f = resource_service.get_filter('storage')
        self.assertEqual(f.normalized_filter(), "resourceType eq 'Microsoft.Storage/storageAccounts'")

    def test_random_azure_resource_filter(self):
        resource_type = 'Microsoft.Network/applicationGateways'
        resource_service = AzureResourceService(None)
        f = resource_service.get_filter(resource_type)
        self.assertEqual(f.normalized_filter(), f"resourceType eq '{resource_type}'")
