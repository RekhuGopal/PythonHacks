from azure.identity import ClientSecretCredential
from azure.core.exceptions import AzureError
import requests

def get_spn_token(tenant_id, client_id, client_secret, scope):
    """
    Fetches an Azure token using Service Principal credentials.

    :param tenant_id: The Azure AD tenant ID.
    :param client_id: The Service Principal (SPN) application ID.
    :param client_secret: The Service Principal (SPN) client secret.
    :param scope: The scope for which the token is requested (e.g., "https://management.azure.com/.default").
    :return: The access token string.
    """
    try:
        # Authenticate using the Service Principal credentials
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )

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

# Example Usage
if __name__ == "__main__":
    # Replace these with your Service Principal credentials and scope
    tenant_id = "<>"
    client_id = "<>"
    client_secret = "<>"
    scope = "https://management.azure.com/.default"

    token = get_spn_token(tenant_id, client_id, client_secret, scope)

    if token:
        print("Access Token:", token)
        print(get_billing_accounts(token))
    else:
        print("Could not retrieve the token.")
