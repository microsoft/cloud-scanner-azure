from .azure_credential_config import AzureCredentialConfig


class AzureResourceServiceConfig:
    """
    Configuration required for usage of AzureResourceService
    """
    def __init__(self, subscription_id, creds: AzureCredentialConfig):
        self.credentials = creds
        self.subscription_id = subscription_id
