provider "azurerm" {
 # The "feature" block is required for AzureRM provider 2.x. 
 # If you're using version 1.x, the "features" block is not allowed.
 version = "~>2.0"
 features {}
 subscription_id = "YOUR_SUBSCRIPTION_ID"
 client_id  = "YOUR_SPN_CLIENT_ID"
 client_secret  = "YOUR_SPN_CLIENT_SECRETE"
 tenant_id       =  "YOUR_TENANT_ID"
}