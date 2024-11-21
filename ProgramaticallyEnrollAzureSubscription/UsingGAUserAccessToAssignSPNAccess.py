from azure.identity import DefaultAzureCredential
from azure.core.exceptions import AzureError
import uuid
import requests

def get_azure_token(scope: str):
    """
    Fetches an Azure token using DefaultAzureCredential.

    :param scope: The scope for which the token is requested (e.g., "https://management.azure.com/.default").
    :return: The access token string.
    """
    try:
        # Instantiate the DefaultAzureCredential
        credential = DefaultAzureCredential()

        # Request a token for the specified scope
        token = credential.get_token(scope)

        print("Token fetched successfully.")
        return token.token
    except AzureError as e:
        print(f"Failed to fetch token: {e}")
        return None

def get_billing_accounts(token):
    """
    Fetches billing accounts from the Azure REST API.

    :param tenant_id: Azure AD tenant ID.
    :param client_id: Service Principal (SPN) application ID.
    :param client_secret: Service Principal (SPN) client secret.
    :return: JSON response containing billing accounts or error message.
    """
 
    try:
       
        # Azure REST API endpoint
        url = "https://management.azure.com/providers/Microsoft.Billing/billingaccounts?api-version=2020-05-01"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Make the GET request
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            print("Billing accounts fetched successfully.")
            return response.json()
        else:
            print(f"Failed to fetch billing accounts. Status code: {response.status_code}")
            return response.json()

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def assign_billing_role( token , billing_account_name, enrollment_account_name, principal_id, principal_tenant_id):
    """
    Assigns a billing role to a principal.
    :param billing_account_name: Billing account name.
    :param enrollment_account_name: Enrollment account name.
    :param principal_id: Azure AD principal (user/service principal) ID.
    :param principal_tenant_id: Azure AD tenant ID of the principal.
    :return: API response as JSON or error message.
    """
    try:
        billing_role_assignment_name = str(uuid.uuid4())
        role_definition_id = "/providers/Microsoft.Billing/billingAccounts/7898901/enrollmentAccounts/225314/billingRoleDefinitions/a0bcee42-bf30-4d1b-926a-48d21664ef71"

        # Azure REST API endpoint
        url = (
            f"https://management.azure.com/providers/Microsoft.Billing/"
            f"billingAccounts/{billing_account_name}/"
            f"enrollmentAccounts/{enrollment_account_name}/"
            f"billingRoleAssignments/{billing_role_assignment_name}?api-version=2019-10-01-preview"
        )

        # Request payload
        payload = {
            "properties": {
                "principalId": principal_id,
                "principalTenantId": principal_tenant_id,
                "roleDefinitionId": role_definition_id
            }
        }

        # HTTP headers
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Make the PUT request
        response = requests.put(url, headers=headers, json=payload)

        # Check if the request was successful
        if response.status_code in [200, 201]:
            print("Billing role assigned successfully.")
            return response.json()
        else:
            print(f"Failed to assign billing role. Status code: {response.status_code}")
            return response.json()

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example Usage
if __name__ == "__main__":
    # Replace this with the required scope
    scope = "https://management.azure.com/.default"
    token = get_azure_token(scope)

    if token:
        print("Access Token:", token)
        print(get_billing_accounts(token))
    else:
        print("Could not retrieve the token.")
