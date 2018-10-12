from cloud_scanner_azure.services.azure_resource import AzureResource
from .unittest_base import TestCase


class TestResourceObject(TestCase):

    def test_azure_resource(self):

        input_azure_dict = {
            "id":"/subscriptions/000000000-0000-0000-0000-db3b8d7d00000/resourceGroups/aasdf-qna/providers/Microsoft.Compute/accounts/asdf-qna",
            "name":"asdf-qna",
            "type":"Microsoft.CognitiveServices/accounts",
            "location":"westus",
            "kind":"QnAMaker",
            "sku":{
                "name":"F0"
            },
            "tags": {
                "Environment": "Production",
                "AppDefined02": "Some app defined thing",
                "AppName": "The app",
                "Name": "Cool Name"
            }
        }

        az_object = AzureResource(input_azure_dict)
        az_normalized = az_object.to_normalized_dict()

        assert(az_normalized["ARN"] == input_azure_dict["id"])
        assert(az_normalized["ResourceId"] == input_azure_dict["name"])
        assert(az_normalized["ResourceType"] == input_azure_dict["type"].replace("/","_").replace(".", "_"))
        assert(az_normalized["Region"] == input_azure_dict["location"])
        assert(az_normalized["Name"] == input_azure_dict["tags"]["Name"])
        assert(az_normalized["AppDefined02"] == input_azure_dict["tags"]["AppDefined02"])
        assert(az_normalized["AppName"] == input_azure_dict["tags"]["AppName"])
        assert(az_normalized["Environment"] == input_azure_dict["tags"]["Environment"])
