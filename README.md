# cloud-scanner-azure

Azure package of adapters for [cloud-scanner]() library. Includes services and their required configurations.

### Running Locally

You can run unit tests in a Python 3.6 virtual environment:

```python
virtualenv env
source env/bin/activate
(env) pip install -r requirements.txt
(env) python -m pytest
```

#### Queue Adapters
- Azure Storage Queue
    - Needs `AZURE_STORAGE_ACCOUNT` and `AZURE_STORAGE_KEY`
    - To use, set environment variable `QUEUE_TYPE=azure_storage_queue`

#### Resource Service Adapters
- Azure Resource Service
    - Needs `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET` and `AZURE_TENANT_ID` of Service Principal
    - If performing actions other than reading, Service Principal needs to be given `Contributor` access or greater

#### Storage Container Adapters
- Azure Blob Storage
    - Needs `AZURE_STORAGE_ACCOUNT` and `AZURE_STORAGE_KEY`
    - To use, set environment variable `STORAGE_CONTAINER_TYPE=azure_storage`

#### Table Storage Adapters
- Azure CosmosDB
    - Needs `COSMOS_TABLE`, `COSMOS_ACCOUNT` and `COSMOS_KEY`
    - To use, set environment variable `RESOURCE_STORAGE_TYPE=azure_cosmos_table`

# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.