import os
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from AzureTestCases.azure_aipolicy_tests import azure_check_if_ai_services_can_be_created_in_allowed_rg
from azure.mgmt.resource.resources.models import DeploymentWhatIf, DeploymentWhatIfProperties

# Read SPNTenant from environment
spn_clnt = os.environ.get("SPNClient")
spn_scrt = os.environ.get("SPNClientSct")
spn_tenant = os.environ.get("SPNTenant")
azure_env = os.environ.get("AzureENV")

# Replace these values with your Azure subscription ID, resource group, and storage account name
if azure_env == "dev":
    SUBSCRIPTION_ID = '063965e0-d141-48d4-b8bd-0dfdc0dc00ff'
    AllowedRG = "costoptimizationsas"
    NotAllowedRG = "testrg"
    RGN = "eastus"
else :
    raise ValueError("Missing one or more required environment variables!")

# Authenticate using ClientSecretCredential (SPN)
credential = ClientSecretCredential(tenant_id=spn_tenant, client_id=spn_clnt, client_secret=spn_scrt)

# Create a Resource Management Client
resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)

## Test the functionality by calling the imported function
def test_azure_check_if_ai_services_can_be_created_in_allowed_rg():
    result = azure_check_if_ai_services_can_be_created_in_allowed_rg(DeploymentWhatIf, DeploymentWhatIfProperties, resource_client, AllowedRG, RGN, 'pyestazureai1')
    assert result == True

def test_azure_check_if_ai_services_can_be_created_in_not_allowed_rg():
    result = azure_check_if_ai_services_can_be_created_in_allowed_rg(DeploymentWhatIf, DeploymentWhatIfProperties, resource_client, NotAllowedRG, RGN, 'pyestazureai2')
    assert result == False