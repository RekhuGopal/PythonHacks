import requests
from azure.identity import DefaultAzureCredential

# Replace with your details
billing_account_id = "614f33a4-c967-4389-b410-ebac6d310c3c"  # Your Billing Account ID
api_version = "2020-01-01"
subscription_name = "MyNewSubscription"  # Desired subscription name
offer_type = "MS-AZR-0017P"  # Example offer type for Pay-As-You-Go

# API URL for creating a subscription
url = f"https://management.azure.com/providers/Microsoft.Billing/billingAccounts/{billing_account_id}/createSubscription?api-version={api_version}"

# Request body for creating a subscription
body = {
    "displayName": subscription_name,
    "skuId": offer_type,
    "owner": {
        "objectId": "d9dc2582-fd85-4167-8d03-f1e62df2aea7",  # Replace with your objectId
        "tenantId": "7ca289b9-c32d-4f01-8566-7ff93261d76f"  # Replace with your tenantId
    }
}

# Authenticate using DefaultAzureCredential
credential = DefaultAzureCredential()
token = credential.get_token("https://management.azure.com/.default")
headers = {
    "Authorization": f"Bearer {token.token}",
    "Content-Type": "application/json"
}

# Make the API request
response = requests.put(url, json=body, headers=headers)

if response.status_code == 200 or response.status_code == 201:
    print("Subscription created successfully!")
    print(response.json())
else:
    print("Failed to create subscription")
    print(f"Status Code: {response.status_code}")
    print(response.json())
