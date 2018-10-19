class AzureStorageConfig:
    """Configuration required for usage of AzureStorage service."""

    def __init__(self, account_name, account_key):
        self.account_name = account_name
        self.account_key = account_key
