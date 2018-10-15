import copy

from cloud_scanner.contracts.resource import Resource
from cloud_scanner_azure.helpers.extractors import ResourceExtractors


class AzureResource(Resource):

    def __init__(self, resource_dict: dict):
        '''
        Create AzureResource from dictionary with necessary values
        :param resource_dict: Dictionary with data like:
        {
            'id': <resource-id>,
            'provider_type': <cloud-provider>
        {
        '''

        d = copy.deepcopy(resource_dict)

        resource_id = d['id']
        d['provider_type'] = "azure"
        d['accountId'] = ResourceExtractors.get_subscription(resource_id)

        self._group = ResourceExtractors.get_resource_group(resource_id)
        d['group'] = self._group

        super().__init__(d)

    @property
    def group(self):
        '''
        Azure Resource Group
        :return: Name of resource group for resource
        '''
        return self._group
