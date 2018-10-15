from azure.common.credentials import ServicePrincipalCredentials
from cloud_scanner.config import Config


class AzureCredentialConfig(Config):
    """
    Configuration required for usage of Azure Credentials
    """

    @property
    def client_id(self):
        """
        Client ID for service principal
        :return: str Client ID
        """
        return self.get_property('AZURE_CLIENT_ID')

    @property
    def client_secret(self):
        """
        Client secret for service principal
        :return: str Client Secret
        """
        return self.get_property('AZURE_CLIENT_SECRET')

    @property
    def tenant_id(self):
        """
        Tenant ID for service principal
        :return: str Tenant ID
        """
        return self.get_property('AZURE_TENANT_ID')

    @property
    def service_principal(self):
        """
        :return: ServicePrincipalCredentials object to be used with Azure SDK
        """
        return ServicePrincipalCredentials(
            self.client_id,
            self.client_secret,
            tenant=self.tenant_id)
