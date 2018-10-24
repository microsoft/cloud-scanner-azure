from azure.mgmt.resource.subscriptions import SubscriptionClient

from cloud_scanner.contracts import AccountService, register_account_service
from cloud_scanner_azure.config.azure_config import (
    AzureConfig, AzureCredentialConfig)


@register_account_service("azure",
                          lambda: AzureSubscriptionService.create())
class AzureSubscriptionService(AccountService):
    """Service to get available subscriptions from Azure."""

    def __init__(self, config: AzureCredentialConfig):
        self._client = None
        self._config = config

    def _get_client(self):
        """
        :return: Azure SubscriptionClient object
        """

        if self._client is None:
            self._client = SubscriptionClient(self._config.service_principal)

        return self._client

    def get_accounts(self):
        """
        :return: List of subscription dictionaries
            with 'subscriptionId' and 'displayName' fields
        """

        return [sub.serialize(True) for sub in
                self._get_client().subscriptions.list()]

    @staticmethod
    def create():
        """
        :return: Initialized AzureSubscriptionService object with
            creds from config
        """

        config = AzureConfig()
        return AzureSubscriptionService(config.credential_config)
