from azure.storage.queue import QueueService, QueueMessageFormat

from cloud_scanner.contracts import Queue, register_queue_service
from cloud_scanner_azure.config.azure_config import (
    AzureConfig, AzureStorageConfig)


@register_queue_service("azure_storage_queue",
                        lambda queue_name:
                        AzureStorageQueue.create(queue_name))
class AzureStorageQueue(Queue):
    """Interface for interacting with an Azure Storage Queue (through the Queue
    contract)"""

    def __init__(self, queue_name, config: AzureStorageConfig):
        """Initializes the storage queue.

        :param queue_name: The name of the queue to access.
        If a queue with this name doesn't already exist on the
        storage account, the queue will be created on the first operation.
        :param config: AzureStorageConfig with a valid account name and
        account key
        """
        self._queue_name = queue_name
        self._queue_service = QueueService(
            account_name=config.account_name, account_key=config.account_key)

        self._queue_service.encode_function = \
            QueueMessageFormat.text_base64encode
        self._queue_service.decode_function = \
            QueueMessageFormat.text_base64decode

    def push(self, message):
        """Pushes a new message onto the queue."""
        self._queue_service.create_queue(self._queue_name)
        self._queue_service.put_message(self._queue_name, message)

    def pop(self):
        """Pops the first message from the queue and returns it."""
        self._queue_service.create_queue(self._queue_name)

        # get_messages prevents another client from getting the message
        # before we've had a chance to delete it. The visibility_timeout
        # prevents the message from being seen by other clients
        # for X seconds.
        messages = self._queue_service.get_messages(
            self._queue_name, visibility_timeout=30)
        for message in messages:
            result = message.content
            self._queue_service.delete_message(
                self._queue_name, message.id, message.pop_receipt)
            return result

    def peek(self):
        """Peeks the fist message from the queue and returns it."""
        self._queue_service.create_queue(self._queue_name)
        messages = self._queue_service.peek_messages(self._queue_name)
        for message in messages:
            return message.content

    @staticmethod
    def create(queue_name: str):
        """Helper function for creating a Azure Storage Queue from the
        storage_config property defined inside of AzureConfig."""
        azure_config = AzureConfig()
        return AzureStorageQueue(queue_name, azure_config.storage_config)
