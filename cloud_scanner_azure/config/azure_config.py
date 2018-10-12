from cloud_scanner.config import Config
from .azure_cosmosdb_config import AzureCosmosDbConfig
from .azure_credential_config import AzureCredentialConfig
from .azure_resource_config import AzureResourceServiceConfig
from .azure_storage_config import AzureStorageConfig


class AzureConfig(Config):
    """
    Azure Configuration class for retrieving Azure-related configuration properties.
    """

    def get_property(self, property_name):
        """
        Override of the base get_property.
        Each property_name has "AZURE_" pre-pended onto it.
        :param property_name: Name of the AZURE_ property to get.
        :return: Property value as a string or None if it doesn't exist.
        """

        normalized_key = f"AZURE_{property_name}"
        return super().get_property(normalized_key)

    @property
    def credential_config(self):
        """
        Gets the default Azure credential config.
        :return: AzureCredentialConfig populated with the AZURE_ CLIENT_ID, TENANT_ID, and CLIENT_SECRET

        """

        return AzureCredentialConfig()

    def get_resource_service_config(self, subscription_id):
        '''
        Creates an AzureResourceServiceConfig for a subscription_id, using the default Azure credential configuration.
        :param subscription_id: The subscription_id the resource service is to target.
        :return: AzureResourceServiceConfig
        '''

        return AzureResourceServiceConfig(
            subscription_id,
            self.credential_config
        )

    @property
    def storage_config(self):
        '''
        Gets the default AzureStorageConfig configuration specified by the AZURE_ STORAGE_ACCOUNT and STORAGE_KEY properties.
        '''

        return AzureStorageConfig(
            self.get_property('STORAGE_ACCOUNT'),
            self.get_property('STORAGE_KEY')
        )

    @property
    def cosmos_storage_config(self):
        '''
        Gets the default AzureCosmosDbConfig configuration specified by the AZURE_ COSMOS_TABLE, COSMOS_ACCOUNT, and COSMOS_KEY properties.
        '''

        return AzureCosmosDbConfig(
            self.get_property('COSMOS_TABLE'),
            AzureStorageConfig(
                self.get_property('COSMOS_ACCOUNT'),
                self.get_property('COSMOS_KEY')
            ))


