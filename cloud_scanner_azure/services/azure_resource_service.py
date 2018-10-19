import logging

from azure.mgmt.resource import ResourceManagementClient

from cloud_scanner.contracts import (
    ResourceService, ResourceFilter, register_resource_service
)
from cloud_scanner_azure.config import AzureConfig, AzureResourceServiceConfig

from .azure_resource import AzureResource


class NoFilter(ResourceFilter):
    """Allows for querying all resources."""

    def normalized_filter(self):
        return None


class AzureResourceTypeFilter(ResourceFilter):
    """Allows for querying all resources."""

    def __init__(self, resource_type):
        self._filter = "resourceType eq '" + resource_type + "'"

    def normalized_filter(self):
        """
        :return: Gets OData string for filtering on resource type
        """
        return self._filter


@register_resource_service('azure',
                           lambda subscription_id:
                           AzureResourceService.create(subscription_id))
class AzureResourceService(ResourceService):
    """Service for querying Azure resources."""

    def __init__(self, config: AzureResourceServiceConfig):
        self._client = None
        self._config = config
        self._resource_type_apis = {}

        self._knownTypes = {
            'vm': 'Microsoft.Compute/virtualMachines',
            'storage': 'Microsoft.Storage/storageAccounts',
            'microsoft.compute/virtualmachines':
                'Microsoft.Compute/virtualMachines',
            'microsoft.storage/storageaccounts':
                'Microsoft.Storage/storageAccounts'
        }

    def _get_client(self):
        """Initializes Azure ResourceManagementClient.

        :return: ResourceManagementClient object
        """
        if self._client is None:
            self._client = ResourceManagementClient(
                self._config.credentials.service_principal,
                self._config.subscription_id)

        return self._client

    @property
    def name(self):
        """Name of cloud provider.

        :return: 'azure'
        """
        return "azure"

    def get_resources(self, filter: ResourceFilter = None):
        """Get resources based on filter.

        :param filter: Filter for resources
        :return: List of AzureResource objects as serialized from client
        """
        resources = self._get_client().resources.list(
            expand="tags", filter=filter.normalized_filter())
        return [AzureResource(resource.serialize(True))
                for resource in resources]

    def get_filter(self, payload):
        """Returns filter object based on payload.

        :param payload: Filter type
        (if payload is one of the resource types, returns
        AzureResourceTypeFilter. No other filter types are
        supported except NoFilter)
        :return: Filter object
        """
        try:
            resource_type = self._knownTypes[payload.lower()]
            return AzureResourceTypeFilter(resource_type)
        except AttributeError:
            return NoFilter()
        except KeyError:
            logging.warning("The filter " + payload +
                            " is not supported and will be ignored")
            return NoFilter()
        except Exception:
            raise NotImplementedError(
                "The payload " + payload + " is not a supported filter")

    def update_resource(self, resource: AzureResource):
        """Updates Azure resource.

        :param resource: AzureResource object to update
        :return:
        """
        api_version = self._resolve_api_for_resource_type(resource.type)
        if api_version is None:
            raise Exception(
                f"Unabled to find api version to update {resource.id}")

        self._get_client().resources.update_by_id(
            resource.id, api_version, resource.to_dict())

    # Internal Helper function to resolve API version to access Azure with
    def _resolve_api_for_resource_type(self, resource_type):
        """Gets API version for resource type.

        :param resource_type: Azure resource type
        :return: API version required for client
        """
        if resource_type in self._resource_type_apis:
            return self._resource_type_apis[resource_type]

        resource_type_info = resource_type.split('/', 1)
        resource_provider = resource_type_info[0]
        resource_provider_type = resource_type_info[1]

        provider = self._get_client().providers.get(resource_provider)
        provider_details = next(
            (t for t in provider.resource_types if
             t.resource_type == resource_provider_type), None)

        if provider_details and 'api_versions' in provider_details.__dict__:
            # Remove preview API versions
            api_version = [v for v in provider_details.__dict__[
                'api_versions'] if 'preview' not in v.lower()]
            # Get most recent remaining API
            chosen_api = api_version[0] if api_version else \
                provider_details.__dict__['api_versions'][0]
            self._resource_type_apis[resource_type] = chosen_api

            return chosen_api

        return None

    @staticmethod
    def create(subscription_id):
        """Instantiate AzureResourceService for specified subscription.

        :param subscription_id: Subscription to manage with service
        :return: AzureResourceService object
        """
        config = AzureConfig()
        return AzureResourceService(
            config.get_resource_service_config(subscription_id))
