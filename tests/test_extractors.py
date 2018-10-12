from .unittest_base import TestCase
from cloud_scanner.helpers import ResourceExtractors


class AzureResourceExtractorTest(TestCase):

    def _test_subscription(self, resource_id, subscription_id):
        found_subscription = ResourceExtractors.get_subscription(resource_id)
        assert(found_subscription == subscription_id)

    def _test_resource_group(self, resource_id, resource_group):
        found_group = ResourceExtractors.get_resource_group(resource_id)
        assert(found_group == resource_group)

    def _test_resource_provider(self, resource_id, provider):
        found_provider = ResourceExtractors.get_resource_provider(resource_id)
        assert(found_provider == provider)

    def _test_resource_type(self, resource_id, resource_type):
        found_type = ResourceExtractors.get_resource_type(resource_id)
        assert(found_type == resource_type)

    def _test_resource(self, resource):
        self._test_subscription(resource['id'], resource['subscription_id'])
        self._test_resource_group(resource['id'], resource['resource_group'])
        self._test_resource_provider(resource['id'], resource['resource_provider'])
        self._test_resource_type(resource['id'],
                                 f"{resource['resource_provider']}/{resource['resource_type']}")

    def _create_resource_id(self, subscription_id=None, resource_group=None, resource_provider=None,
                            resource_type=None, resource_name=None):
        subscription_id = "808b8977-950a-4a96-8229-b48d708aa455" if not subscription_id else subscription_id
        resource_group = "myResourceGroup" if not resource_group else resource_group
        resource_provider = "Microsoft.Compute" if not resource_provider else resource_provider
        resource_type = "virtualMachines" if not resource_type else resource_type
        resource_name = "myResourceName" if not resource_name else resource_name

        resource_id = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/" \
                      f"{resource_provider}/{resource_type}/{resource_name}"

        resource_data = {
            'id': resource_id,
            'subscription_id': subscription_id,
            'resource_group': resource_group,
            'resource_provider': resource_provider,
            'resource_type': resource_type,
            'resource_name': resource_name
        }

        return resource_data

    def test_basic(self):
        resource = self._create_resource_id()
        self._test_resource(resource)
