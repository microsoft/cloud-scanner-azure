from azure.cosmosdb.table.tableservice import TableService

from cloud_scanner.contracts import register_resource_storage, TableStorage
from cloud_scanner.helpers import entry_storage
from cloud_scanner_azure.config import AzureCosmosDbConfig, AzureConfig


@register_resource_storage('azure_cosmos_table', lambda: AzureCosmosDb.create())
class AzureCosmosDb(TableStorage):
    '''
    Azure CosmosDB provider for Table Storage
    '''

    def __init__(self, config:AzureCosmosDbConfig):
        self._table_service = TableService(account_name=config.account_name, account_key=config.account_key)
        self._tableName = config.table_name

    def check_entry_exists(self, entry):
        '''
        Check if entry exists in table
        :param entry: Dictionary formatted as:
        {
            'PartitionKey': ...,
            'RowKey': ...
        }
        :return: True if entry exists
        '''
        try:
            self.query(entry['PartitionKey'], entry['RowKey'])
            return True
        except:
            return False

    def write(self, resource):
        '''
        Write resource to table
        :param resource: Expecting Resource object (see Common.Contracts.Resource)
        :return: None
        '''
        entry = resource.to_dict()
        prepared = entry_storage.EntryOperations.prepare_entry_for_insert(entry)

        if not self.check_entry_exists(prepared):
            self._table_service.insert_entity(self._tableName, prepared)
        else:
            self._table_service.update_entity(self._tableName, prepared)

    def query(self, partition_key, row_key):
        '''
        Get entry with specified partition and row keys
        :param partition_key: Partition key for entry
        :param row_key: Row key for entry
        :return: Entity if found, None otherwise
        '''
        task = self._table_service.get_entity(self._tableName, partition_key, row_key)
        return task

    def query_list(self):
        '''
        Get entities from table
        :return: List of entities from table
        '''
        return self._table_service.query_entities(self._tableName)

    def delete(self, partition_key, row_key):
        '''
        Delete entry with specified partition and row keys
        :param partition_key: Partition key for entry
        :param row_key: Row key for entry
        :return: None
        '''
        self._table_service.delete_entity(self._tableName, partition_key, row_key)

    @staticmethod
    def create():
        '''
        Initialize AzureCosmosDb service
        :return: AzureCosmosDb service object
        '''
        config = AzureConfig()
        cosmos_storage = AzureCosmosDb(config.cosmos_storage_config)

        return cosmos_storage
