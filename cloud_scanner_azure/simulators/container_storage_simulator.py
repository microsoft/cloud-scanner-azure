import logging

from cloud_scanner.contracts.storage_container import StorageContainer
from cloud_scanner.contracts.storage_container_factory import register_storage_container


class MockBlobStorageOutput:
    def __init__(self, name, content):
        self._name = name
        self._content = str(content)

    @property
    def name(self):
        return self._name

    @property
    def content(self):
        return self._content

@register_storage_container("simulator", lambda: MockBlobStorageSimulator())
class MockBlobStorageSimulator(StorageContainer):
    def __init__(self):

        config_content = '''{
            "providers":[
                {
                    "type":"simulator",
                    "resourceTypes": [{"typeName": "Microsoft.Compute/virtualMachines"}],
                    "subscriptions": [
                        {
                            "subscriptionId": "00000000-0000-0000-0000-000000000001", 
                            "displayName": "Simulator Sub 1"
                        },
                        {
                            "subscriptionId": "00000000-0000-0000-0000-000000000002", 
                            "displayName": "Simulator Sub 2"
                        }
                    ]
                }]
        }'''

        list_of_entries = []
        latest = MockBlobStorageOutput('config-2018-08-29-10-20-49.json ', config_content)
        entry1 = MockBlobStorageOutput('config-2018-08-20-12-33-48.json ', '{}')
        entry2 = MockBlobStorageOutput('config-2018-08-21-09-41-05.json ', '{}')
        entry3 = MockBlobStorageOutput('config-2018-08-21-09-42-12.json ', '{}')
        entry4 = MockBlobStorageOutput('config-2018-08-22-11-41-49.json ', '{}')
        entry5 = MockBlobStorageOutput('config-2018-08-22-11-50-38.json ', '{}')

        list_of_entries.append(latest)
        list_of_entries.append(entry1)
        list_of_entries.append(entry2)
        list_of_entries.append(entry3)
        list_of_entries.append(entry4)
        list_of_entries.append(entry5)

        self._entries = list_of_entries
        self._latest_entry = latest

    def get_blob_to_text(self, config):
        # ensure the latest config was picked
        if config is not self._latest_entry.name:
            logging.error("The picked config is not the latest. Returned: %s, latest: %s",
                          config, self._latest_entry.name)
            return None
        return self._latest_entry

    def list_blobs(self):
        return self._entries

    def get_latest_config(self):
        return self._latest_entry

    def upload_text(self, filename, text):
        raise logging.warning("upload_text was called.")
