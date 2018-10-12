from azure.common.credentials import ServicePrincipalCredentials
from cloud_scanner.config import Config


class AzureCredentialConfig(Config):

    @property
    def client_id(self):
        return self.get_property('AZURE_CLIENT_ID')

    @property
    def client_secret(self):
        return self.get_property('AZURE_CLIENT_SECRET')

    @property
    def tenant_id(self):
        return self.get_property('AZURE_TENANT_ID')

    @property
    def service_principal(self):
        return ServicePrincipalCredentials(
            self.client_id,
            self.client_secret,
            tenant=self.tenant_id)
