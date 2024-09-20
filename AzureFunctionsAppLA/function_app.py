import azure.functions as func
import logging
import random
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
credential =  DefaultAzureCredential()
subscription_id = "285a9b29-43df-4ebf-85b1-61bbf7929871"
resource_client = ResourceManagementClient(credential, subscription_id)
RESOURCE_GROUP_NAME = "PythonAzureExample-Storage-rg"
LOCATION = "centralus"


app = func.FunctionApp(http_auth_level=func.AuthLevel.ADMIN)

@app.route(route="GetAllAzureResources")
def GetAllAzureResources(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
        DemoAzureResourceCreation()
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

def DemoAzureResourceCreation():
    try:
        # Step 1: Provision the resource group.
        rg_result = resource_client.resource_groups.create_or_update(RESOURCE_GROUP_NAME, { "location": LOCATION })

        print(f"Provisioned resource group {rg_result.name}")

        # Step 2: Provision the storage account, starting with a management object.
        storage_client = StorageManagementClient(credential, subscription_id)

        STORAGE_ACCOUNT_NAME = f"pythonazurestorage{random.randint(1,100000):05}"

        availability_result = storage_client.storage_accounts.check_name_availability({ "name": STORAGE_ACCOUNT_NAME })

        if not availability_result.name_available:
            print(f"Storage name {STORAGE_ACCOUNT_NAME} is already in use. Try another name.")
            exit()

        poller = storage_client.storage_accounts.begin_create(RESOURCE_GROUP_NAME, STORAGE_ACCOUNT_NAME,
            {
                "location" : LOCATION,
                "kind": "StorageV2",
                "sku": {"name": "Standard_LRS"}
            }
        )

        account_result = poller.result()
        print(f"Provisioned storage account {account_result.name}")


        # Step 3: Retrieve the account's primary access key and generate a connection string.
        keys = storage_client.storage_accounts.list_keys(RESOURCE_GROUP_NAME, STORAGE_ACCOUNT_NAME)

        print(f"Primary key for storage account: {keys.keys[0].value}")

        conn_string = f"DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={keys.keys[0].value}"

        print(f"Connection string: {conn_string}")

        # Step 4: Provision the blob container in the account (this call is synchronous)
        CONTAINER_NAME = "cloudquicklabs"
        container = storage_client.blob_containers.create(RESOURCE_GROUP_NAME, STORAGE_ACCOUNT_NAME, CONTAINER_NAME, {})

        print(f"Provisioned blob container {container.name}")
    except:
        print("An exception occurred")